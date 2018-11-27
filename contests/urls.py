from django.urls import path
from . import views

app_name = "contests"

urlpatterns = [
	### EVERYWHERE(IN VIEWS) IT IS contest_unique_code INSTEAD OF contest_unique_id
    path('create', views.create_contest, name="contest-create"),
    path('<slug:contest_unique_code>/edit', views.edit_contest, name="contest-edit"),
    path('<slug:contest_unique_code>/contests/create', views.contest_question_create, name="contest-question-create"),
    path('<slug:contest_unique_code>/contests/<slug:question_unique_code>/edit', views.contest_question_edit, name="contest-question-edit"),

    path('<slug:contest_unique_code>/view', views.view_contest_page)


]