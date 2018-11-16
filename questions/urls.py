from django.urls import path
from . import views

app_name = "questions"

urlpatterns = [
    path('browse', views.browse_questions, name="browse"),
    path('<slug:question_unique_id>/submit', views.submit_solution, name="submit-solution"),
    path('<slug:question_unique_id>/submission/<int:submission_id>/result', views.submission_result, name="submission-result"),
    path('ajax/submission-result', views.ajax_get_submission_results, name="ajax-submission-result")
]