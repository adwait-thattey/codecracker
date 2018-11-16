from django.http import JsonResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from questions.models import Question, Submission, Result
from .forms import SubmissionForm

from .background_tasks import RunAndAssert


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

def result(request):
    return render(request,'questions/results.html')
