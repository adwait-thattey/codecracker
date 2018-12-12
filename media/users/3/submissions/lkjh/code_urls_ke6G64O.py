from django.urls import path

from . import views



urlpatterns = [
    path ('profile_stats',views.profile_stats,name= "Profile_stats"),
    path('profile_stats_pie', views.profile_stats_pie,name = "Profile_stats_pie")
    ]