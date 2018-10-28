from django.shortcuts import render


# Create your views here.
def submit_solution(request, question_unique_id):
    # question
    return render(request, "questions/submit_solution.html")


def submission_result(request, question_unique_id, result_id):
    return render(request, "questions/submission_result.html")
