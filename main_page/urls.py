from django.urls import path

from . import views

app_name = "mainpage"

urlpatterns = [
    path('index', views.landing_page, name='landing'),
    path('home', views.home, name='home'),
    path('', views.redirect_to_landing),
    path('nav', views.nav, name='nav'),
    path('get_notifications', views.notification ,name="Notifications")

    # TODO Change this to switch between landing and home based on user login status later if required

]
