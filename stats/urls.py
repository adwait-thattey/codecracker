from django.urls import path

from stats import views

app_name = "stats"

urlpatterns=[
    path('user-submission-stats/<str:username>', views.user_submission_date_stats, name="user-submission-stats"),
    path('temp-stats-display', views.chart)

]