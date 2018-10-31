from django.http import JsonResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from questions.models import Question, Submission
from .forms import SubmissionForm

# Create your views here.
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

            return redirect('questions:submission-result', question.unique_code, submission.id )

    submission_form = SubmissionForm()
    return render(request, "questions/submit_solution.html", {"form":submission_form})


def submission_result(request, question_unique_id, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)

    return render(request, "questions/submission_result.html", {"submission":submission})

def ajax_get_submission_results(request):
    submission_id = request.GET.get("submission_code", None)
    if submission_id:
        submission = get_object_or_404(Submission, id=submission_id)
        submission_results = list()
        for r in submission.result_set.all():
                d = {
                    "id": str(r.id),
                    "pass_fail": str(r.pass_fail)
                }

                submission_results.append(d)

        total_score = submission.total_score

        data = {
            'results': submission_results,
            'score': total_score
        }

        return JsonResponse(data)
    else:
        raise Http404("Invalid request!")



