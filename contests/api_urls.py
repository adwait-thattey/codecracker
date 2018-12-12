from django.urls import path

from . import api_views


urlpatterns = [
    path('create',api_views.Create_Contest.as_view()),
    path('<slug:contest_unique_id>/edit', api_views.Edit_Contest.as_view()),
    path('<slug:contest_unique_id>/questions/create', api_views.contest_question_create.as_view()),
    path('<slug:contest_unique_id>/questions/<slug:question_unique_id>/edit', api_views.contest_question_edit.as_view()),

]