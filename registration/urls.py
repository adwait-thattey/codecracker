from django.urls import path

from django.contrib.auth import views as auth_views

from . import views
app_name = "registration"
urlpatterns = [
    path('login', auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path('register', views.signup, name='signup'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
]

