from django.urls import path
from . import views

app_name = "contests"

urlpatterns = [
    ### EVERYWHERE(IN VIEWS) IT IS contest_unique_code INSTEAD OF contest_unique_id
    path('create', views.create_contest, name="contest-create"),
    path('<slug:contest_unique_id>/edit', views.edit_contest, name="contest-edit"),
    path('<slug:contest_unique_id>/questions/create', views.contest_question_create, name="contest-question-create"),
    path('<slug:contest_unique_id>/questions/<slug:question_unique_id>/edit', views.contest_question_edit,
         name="contest-question-edit"),
    path('<slug:contest_unique_code>/view', views.view_contest_page, name="view-contest"),
    path('<slug:contest_unique_code>/leaderboard', views.leaderboard, name="leaderboard"),
    path('browse', views.browse_contests, name="browse")

]
