from django.urls import path

from django.conf.urls import handler500

from . import views



urlpatterns = [
    path('index', views.landing_page, name='landing'),
    path('home', views.home, name='home'),
    path('', views.redirect_to_landing),
    path('nav', views.nav, name='nav'),
    path('ajax/get_all_notifications', views.get_all_notifications ,name="all_notifications"),
    path('ajax/get_unseen_notifications', views.get_unseen_notifications, name="unseen_notifications"),
    path('503', views.error_500, name="raise-503"),
    path('404', views.error_404, name="raise-404")
    # TODO Change this to switch between landing and home based on user login status later if required

]

