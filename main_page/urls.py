from django.urls import path

from . import views

urlpatterns = [
    path('index', views.landing_page, name='landing'),
    path('home', views.home, name='home'),
    path('', views.redirect_to_landing)
    # TODO Change this to switch between landing and home based on user login status later if required

]