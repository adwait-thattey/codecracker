from django.urls import path

from django.contrib.auth import views as auth_views
import django.contrib.auth.views
from django.contrib.auth import views as auth_views


from . import views
app_name = "registration"
urlpatterns = [

    path('login', django.contrib.auth.views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path('register', views.signup, name= 'signup'),
    path('password_reset/', auth_views.password_reset, name='password_reset'),
    path('password_reset/done/', auth_views.password_reset_done, name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', auth_views.password_reset_complete, name='password_reset_complete'),

    ]