from time import sleep
from django.http import JsonResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from questions.docker import Docker
from questions.models import Question, Submission, Result, TestCase, Category, QuestionView
from questions.utils import run_in_background
from .forms import SubmissionForm, TestCaseCreateForm, PostQuestionForm, QuestionsFilterForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .background_tasks import RunAndAssert, LimitThreads, SubmissionRunnerController, RunAndReCalc, Scheduler

from django.forms import modelformset_factory
from registration.views import email_confirmation_required





# Create your views here.
def start_code_run_sequence(submission):
    # WARNING DO NOT MAKE THIS ASYNC PROCESS. THE RESULT WILL NOT RENDER IN RESULTS PAGE
    Result.objects.filter(submission=submission).delete()

    for testcase in submission.question.testcase_set.all():
        R = Result.objects.create(testcase=testcase, submission=submission)

    controller = SubmissionRunnerController(thread_id=submission.id, submission=submission)

    controller.start()


@login_required
@email_confirmation_required
def post_question(request):
    if (request.method == "POST"):
        form = PostQuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            return redirect('questions:testcase-view', question.unique_code)
    else:
        form = PostQuestionForm()
    print(form.errors)
    return render(request, "questions/post_question.html", {'form': form})


@login_required
@email_confirmation_required
def edit_question(request, question_unique_id=None):
    instance = get_object_or_404(Question, unique_code=question_unique_id)
    if instance.author != request.user:
        return PermissionDenied("You can not edit this question!")
    form = PostQuestionForm(request.POST or None, instance=instance, initial={"category":instance.category})
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect('questions:view_the_question', instance.unique_code)
    context = {
        'instance': instance,
        'form': form
    }
    return render(request, "questions/post_question.html", context)


@run_in_background
def rerun_all_testcase_submissions(testcase):
    R_set = Result.objects.filter(testcase=testcase)
    R_set.delete()

    thread_list = list()
    for submission in testcase.question.submission_set.all():
        R = Result.objects.create(testcase=testcase, submission=submission)
        thread_temp = RunAndReCalc(thread_id=testcase.id, result_instance=R)
        thread_list.append(thread_temp)

    thread_chunk = Scheduler(threadlist=thread_list)
    thread_chunk.run()

    # TODO Send mail after all submissions have been re-run
    print("done!")


@login_required
@email_confirmation_required
def submit_solution(request, question_unique_id):
    # question
    question = get_object_or_404(Question, unique_code=question_unique_id)
    if hasattr(question,'contestquestion'):
        if question.contestquestion.contest.status!=1:
            return HttpResponse("Contest Has Ended!. You can not submit any more solutions")

    if request.method == "POST":
        submission_form = SubmissionForm(request.POST, request.FILES)

        if submission_form.is_valid():
            submission = submission_form.save(commit=False)
            submission.user = request.user
            submission.question = question
            submission.save()

            start_code_run_sequence(submission)
            return redirect('questions:submission-result', question.unique_code, request.user.username,
                            submission.attempt_number)

    else:
        submission_form = SubmissionForm()
    return render(request, "questions/submit_solution.html", {"form": submission_form})


@login_required
@email_confirmation_required
def submission_result(request, question_unique_id, username, submission_attempt):
    submission = get_object_or_404(Submission,
                                   user__username=username,
                                   question__unique_code=question_unique_id,
                                   attempt_number=submission_attempt)

    return render(request, "questions/results.html", {"submission": submission})


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


def browse_args_questions(request, category, sortby, rev):
    if not Category.objects.filter(pk=category).exists():
        category = 0

    if not sortby in [1, 2, 3, 4]:
        sortby = 1

    if not rev in [0, 1]:
        rev = 0

    questions = Question.objects.all()

    if category != 0:
        questions = questions.filter(category__pk=category)

    if sortby == 1:
        questions = questions.order_by('-create_timestamp')
    elif sortby == 2:
        questions = questions.order_by('submission__count')
    elif sortby == 2:
        questions = questions.order_by('-create_timestamp')
    elif sortby == 2:
        questions = questions.order_by('-create_timestamp')


def browse_questions(request):
    questions = Question.objects.filter(active=True)

    page = request.GET.get('page', 1)
    question_filter_form = QuestionsFilterForm(request.GET)

    question_filter_form.is_valid()
    # Just did this to make sure clean is called

    if "category" in question_filter_form.cleaned_data:
        if question_filter_form.cleaned_data["category"]: #make sure incoming value is not none
            questions = questions.filter(category=question_filter_form.cleaned_data["category"])
    if "sort_by" in question_filter_form.cleaned_data:
        # print("sortby",question_filter_form.cleaned_data["sort_by"])
        sort_by_dict = {
            "1": "-create_timestamp",
            "2": "-submission_count",
            "3": "-view_count",
            "4": "-difficulty"
        }
        questions = questions.order_by(sort_by_dict[question_filter_form.cleaned_data["sort_by"]])
    if "query" in question_filter_form.cleaned_data:
        if question_filter_form.cleaned_data["query"] != 'None':
            # print("query", question_filter_form.cleaned_data["query"])
            questions = questions.filter(title__contains=question_filter_form.cleaned_data["query"])
    if "reverse" in question_filter_form.cleaned_data:
        print(question_filter_form.cleaned_data["reverse"])
        if question_filter_form.cleaned_data["reverse"]:
            questions = questions.reverse()

    paginator = Paginator(questions, 7)
    try:
        sleep(1.5)
        question_page = paginator.page(page)
    except PageNotAnInteger:
        question_page = paginator.page(1)
    except EmptyPage:
        question_page = paginator.page(paginator.num_pages)
    # print(question_page)
    return render(request, "questions/browsequestions3.html",
                  {"questions": question_page, "filter_form": question_filter_form})


def view_the_question(request, question_unique_id):
    question = get_object_or_404(Question, unique_code=question_unique_id)
    if request.user.is_authenticated:
        if not QuestionView.objects.filter(question=question, user=request.user).exists():
            QuestionView.objects.create(question=question, user=request.user)
            question.view_count += 1
            question.save()

    submission_form = SubmissionForm()
    return render(request, "questions/viewing_the_question.html",
                  {"question": question, "submission_form": submission_form})


@login_required
@email_confirmation_required
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


@login_required
@email_confirmation_required
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


@login_required
@email_confirmation_required
def view_testcases(request, question_unique_id):
    question = get_object_or_404(Question, unique_code=question_unique_id)

    if question.author != request.user:
        raise PermissionDenied("You do not have the permission to view this question's meta data")

    testcases = question.testcase_set.all()

    return render(request, "questions/testcases_view.html", {"testcases": testcases, "question": question})


def redirect_to_view_testcases(request, question_unique_id):
    return redirect('questions:testcase-view', question_unique_id)


@login_required
@email_confirmation_required
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


def ajax_call_rerun_all_testcase_submissions(request, question_unique_id):
    ret_data = {"success": False}
    question = Question.objects.filter(unique_code=question_unique_id)
    try:
        test_case_number = int(request.POST.get("test_case_number", None))
        if question.exists():
            question = question[0]
            if question.author == request.user:
                testcase = question.testcase_set.filter(number=test_case_number)
                if testcase.exists():
                    testcase = testcase[0]
                    rerun_all_testcase_submissions(testcase)
                    ret_data["success"] = True

    except:
        pass
    return JsonResponse(ret_data)


# def question_view_count(request):
#     #qview_count= Statistics.objects.question_view_count
#     if request.user.is_authenticated():
#         Statistics.objects.all()


# def submissions_count(request, submissions):
#    if request.
def redirect_to_browse(request):
    return redirect('questions:browse')



def get_question_titles(request):
    q_titles = list(Question.objects.all().values_list('title'))

    ret_dict = {
        'titles': q_titles
    }

    return JsonResponse(ret_dict)

#
#
# API Views below
#
#


def say_hello():
    return HttpResponse("Hello")

