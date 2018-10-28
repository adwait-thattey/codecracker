from django.urls import path
from . import views

app_name = "questions"

urlpatterns = [
    path('<slug:question_unique_id>/submit', views.submit_solution, name="submit-solution"),
    path('<slug:question_unique_id>/submission/<int:result_id>', views.submission_result, name="submission-result")
]