from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = "questions"

urlpatterns = [
    path('', views.redirect_to_browse),
    path('browse', views.browse_questions, name="browse"),
    path('browse/<int:category>/<int:sortby>/<int:rev>', views.browse_args_questions,name="browse_args"),
    path('<slug:question_unique_id>/submit', views.submit_solution, name="submit-solution"),

    path('<slug:question_unique_id>/<str:username>/submission/<int:submission_attempt>/result', views.submission_result, name="submission-result"),
    path('ajax/submission-result', views.ajax_get_submission_results, name="ajax-submission-result"),
    path('<slug:question_unique_id>/view/', views.view_the_question, name="view_the_question"),
    path('post/', views.post_question, name="post_question"),
    path('<slug:question_unique_id>/edit', views.edit_question, name="question-edit"),
    path('<slug:question_unique_id>/testcases/view', views.view_testcases, name="testcase-view"),
    path('<slug:question_unique_id>/testcases/', views.redirect_to_view_testcases),
    path('<slug:question_unique_id>/testcases/new', views.create_testcase, name="testcase-create"),
    path('<slug:question_unique_id>/testcase/<int:test_case_number>/edit', views.edit_testcase, name="testcase-edit"),
    path('<slug:question_unique_id>/testcase/<int:test_case_number>/delete', views.delete_test_case,
         name="delete-testcase"),
    
    
    # path('<slug:question_unique_id>/testcases/edit', views.edit_testcases, name="testcase-edit"),
    path('ajax/submission-result', views.ajax_get_submission_results, name="ajax-submission-result"),
    path('ajax/rerun_test_case_submissions/<slug:question_unique_id>', views.ajax_call_rerun_all_testcase_submissions,
         name="rerun-testcase-submissions"),



]

urlpatterns = format_suffix_patterns(urlpatterns)
