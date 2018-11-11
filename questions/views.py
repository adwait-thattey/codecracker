from django.http import JsonResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from questions.models import Question, Submission, Result, TestCase
from .forms import SubmissionForm, TestCaseCreateForm

from .background_tasks import RunAndAssert

from django.forms import modelformset_factory


# Create your views here.
def start_code_run_sequence(submission):
    # WARNING DO NOT MAKE THIS ASYNC PROCESS. THE RESULT WILL NOT RENDER IN RESULTS PAGE
    for testcase in submission.question.testcase_set.all():
        R = Result.objects.create(testcase=testcase, submission=submission)
        thread_temp = RunAndAssert(thread_id=testcase.id, result_instance=R)
        thread_temp.start()


@login_required
def submit_solution(request, question_unique_id):
    # question
    question = get_object_or_404(Question, unique_code=question_unique_id)
    if request.method == "POST":
        submission_form = SubmissionForm(request.POST, request.FILES)

        if submission_form.is_valid():
            submission = submission_form.save(commit=False)
            submission.user = request.user
            submission.question = question
            submission.save()

            start_code_run_sequence(submission)
            return redirect('questions:submission-result', question.unique_code, submission.id)

    else:
        submission_form = SubmissionForm()
    return render(request, "questions/submit_solution.html", {"form": submission_form})


def submission_result(request, question_unique_id, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)

    return render(request, "questions/submission_result.html", {"submission": submission})


def ajax_get_submission_results(request):
    submission_id = request.GET.get("submission_code", None)
    if submission_id:
        submission = get_object_or_404(Submission, id=submission_id)

        submission_results = [r.as_dict() for r in submission.result_set.all()]

        total_score = submission.total_score

        data = {
            'results': submission_results,
            'score': total_score
        }

        return JsonResponse(data)
    else:
        raise Http404("Invalid request!")


@login_required
def create_testcase(request, question_unique_id):
    question = get_object_or_404(Question, unique_code=question_unique_id)
    if question.author != request.user:
        raise PermissionDenied("You do not have the permission to edit this question's meta data")

    num_test_cases = question.testcase_set.count()
    print(num_test_cases)
    if num_test_cases >= 10:
        return HttpResponse("Currently we do not support more than 10 test cases for 1 question.")

    if request.method == "POST":
        test_case_form = TestCaseCreateForm(request.POST, request.FILES)

        if test_case_form.is_valid():
            test_case = test_case_form.save(commit=False)
            test_case.question = question
            test_case.number = num_test_cases + 1
            test_case.save()

            add_another = request.POST.get("add-another", 0)
            try:
                add_another = int(add_another)
            except ValueError:
                add_another = 0

            if add_another == 1:
                return redirect('questions:testcase-create', question_unique_id)
            else:
                return redirect('questions:testcase-view', question_unique_id)



    else:
        test_case_form = TestCaseCreateForm()

    return render(request, "questions/create_test_case.html",
                  {"test_case_form": test_case_form, "new_case_number": num_test_cases + 1})


def edit_testcase(request, question_unique_id, test_case_number):
    question = get_object_or_404(Question, unique_code=question_unique_id)
    if question.author != request.user:
        raise PermissionDenied("You do not have the permission to edit this question's meta data")

    test_case_q_set = question.testcase_set.filter(number=int(test_case_number))
    if test_case_q_set.exists():
        test_case = test_case_q_set[0]
    else:
        raise Http404("This Test Case Does Not exist!")

    if request.method == "POST":
        test_case_form = TestCaseCreateForm(request.POST, request.FILES, instance=test_case)

        if test_case_form.is_valid():
            test_case = test_case_form.save(commit=False)
            test_case.save()
            return redirect('questions:testcase-view', question_unique_id)



    else:
        test_case_form = TestCaseCreateForm(instance=test_case)

    return render(request, "questions/edit_test_case.html",
                  {"test_case_form": test_case_form, "new_case_number": test_case.number})


def view_testcases(request, question_unique_id):
    question = get_object_or_404(Question, unique_code=question_unique_id)

    if question.author != request.user:
        raise PermissionDenied("You do not have the permission to view this question's meta data")

    testcases = question.testcase_set.all()

    return render(request, "questions/testcases_view.html", {"testcases": testcases, "question":question})


def redirect_to_view_testcases(request, question_unique_id):
    return redirect('questions:testcase-view', question_unique_id)


def delete_test_case(request, question_unique_id, test_case_number):
    question = get_object_or_404(Question, unique_code=question_unique_id)
    if question.author != request.user:
        raise PermissionDenied("You do not have the permission to delete this question's meta data")

    test_case_q_set = question.testcase_set.filter(number=int(test_case_number))
    if test_case_q_set.exists():
        test_case = test_case_q_set[0]
    else:
        raise Http404("This Test Case Does Not exist!")

    test_case.delete()

    return redirect('questions:testcase-view', question_unique_id)
