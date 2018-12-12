from django.urls import path

from django.contrib.auth import views as auth_views

from . import views
app_name = "registration"
urlpatterns = [
    path('login', auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path('register', views.signup, name='signup'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('logout', views.logout_view, name='logout'),
    path('google_log_in', views.google_sign_in, name="google_sign_in"),
    path('profile', views.profile, name='profile'),
    path('resend_activation_link', views.generate_new_activation_link, name="resend_activation_link")
]
