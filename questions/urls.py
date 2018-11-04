from django.urls import path
from . import views

app_name = "questions"

urlpatterns = [
    path('<slug:question_unique_id>/submit', views.submit_solution, name="submit-solution"),
    path('<slug:question_unique_id>/submission/<int:submission_id>/result', views.submission_result, name="submission-result"),
    path('<slug:question_unique_id>/testcases/create', views.create_testcases, name="testcase-create"),
    path('<slug:question_unique_id>/testcases/edit', views.edit_testcases, name="testcase-edit"),
    path('ajax/submission-result', views.ajax_get_submission_results, name="ajax-submission-result")
]