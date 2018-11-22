from django.urls import path

from . import views



urlpatterns = [
    path('index', views.landing_page, name='landing'),
    path('home', views.home, name='home'),
    path('', views.redirect_to_landing),
    path('nav', views.nav, name='nav'),
    path('ajax/get_all_notifications', views.get_all_notifications ,name="all_notifications"),
    path('ajax/get_unseen_notifications', views.get_unseen_notifications, name="unseen_notifications")

    # TODO Change this to switch between landing and home based on user login status later if required

]
