from django.urls import path
from . import views

app_name = "contests"

urlpatterns = [
    path('create', views.create_contest, name="contest-create"),
    path('<slug:contest_unique_id>/edit', views.edit_contest, name="contest-edit"),
    path('<slug:contest_unique_id>/questions/create', views.contest_question_create, name="contest-question-create"),
    path('<slug:contest_unique_id>/questions/<slug:question_unique_id>/edit', views.contest_question_edit, name="contest-question-edit"),


]