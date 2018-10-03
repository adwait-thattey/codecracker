from django.urls import path

from . import views

urlpatterns = [
    path('', views.landing_page, name='landing'),
    # TODO Change these both to switch between landing and home based on user login status later if required
    path('home', views.home, name='home'),
]