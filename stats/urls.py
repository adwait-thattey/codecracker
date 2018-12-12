from django.urls import path

from stats import views

app_name = "stats"

urlpatterns=[
    path('user-submission-stats/<str:username>', views.user_submission_date_stats, name="user-submission-stats"),
    path('user-question-attempts-stats/<str:username>', views.user_question_attempts_stats, name="user-question-attempts-stats"),
    path('user-submission-percentage-stats/<str:username>', views.user_submission_percentage, name="user-submission-percentage-stats"),
    path('user-avg-attempts-per-question-stats/<str:username>', views.user_avg_attempts_per_question, name="user-avg-attempts-per-question-stats"),
    path('user-per-question-attempts-stats/<str:username>', views.user_per_question_attempts_stats, name="user-per-question-attempts-stats"),
    path('temp-stats-display', views.chart),
    path('temp-stats-display-pie',views.display_pie),

]