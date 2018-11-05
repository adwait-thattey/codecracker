from django.urls import path
from . import views

app_name = "questions"

urlpatterns = [
    path('<slug:question_unique_id>/submit', views.submit_solution, name="submit-solution"),
    path('<slug:question_unique_id>/submission/<int:submission_id>/result', views.submission_result, name="submission-result"),
    path('ajax/submission-result', views.ajax_get_submission_results, name="ajax-submission-result"),
    path('question/', views.view_the_question, name="view_the_question")
]