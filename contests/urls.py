from django.urls import path
from . import views

app_name = "contests"

urlpatterns = [
    ### EVERYWHERE(IN VIEWS) IT IS contest_unique_code INSTEAD OF contest_unique_id
    path('create', views.create_contest, name="contest-create"),
    path('<slug:contest_unique_id>/edit', views.edit_contest, name="contest-edit"),
    path('<slug:contest_unique_id>/questions/create', views.contest_question_create, name="contest-question-create"),

    path('<slug:contest_unique_id>/participants',views.participants,name="contest-participants"),

    path('<slug:contest_unique_id>/questions/<slug:question_unique_id>/edit', views.contest_question_edit,
         name="contest-question-edit"),
    path('<slug:contest_unique_code>/view', views.view_contest_page, name="view-contest"),
    path('browse', views.browse_contests, name="browse"),
    path('<slug:contest_unique_id>/register', views.register_for_contest, name="register"),
    path('<slug:contest_unique_id>/unregister', views.unregister_from_contest, name="unregister"),
    path('<slug:contest_unique_id>/refresh_contest_state', views.refresh_contest_state, name="refresh"),
    path('<slug:contest_unique_id>/register_from_author', views.register_user_from_author, name="author-register-user")


]
