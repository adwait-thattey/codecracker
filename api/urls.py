from django.urls import path, include

app_name = "api"

urlpatterns=[
    path('questions/', include('questions.api_urls')),
    path('contests/', include('contests.api_urls')),
]