"""ase1_prj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls import handler500, url
from rest_framework.documentation import include_docs_urls

from main_page import views as main_views
from rest_framework_jwt.views import obtain_jwt_token


urlpatterns = [

    path('', include('main_page.urls')),
    path('admin/', admin.site.urls),
    path('registration/', include('registration.urls')),
    path('questions/', include('questions.urls')),
    path('contests/', include('contests.urls')),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="registration/password_reset_form.html"),
         name='password_reset'),

    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"),
         name='password_reset_complete'),

    path('ckeditor/', include('ckeditor_uploader.urls')),

    path('stats/', include('stats.urls')),

    path('api-token-auth/', obtain_jwt_token),
    path('api/', include('api.urls')),
    path('docs/', include_docs_urls(title="CodeCracker REST API"))
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# handler404 = 'main_views.error_404'
handler500 = main_views.error_500

# if settings.DEBUG == False:
#     urlpatterns += patterns('',
#         url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
#             'document_root': settings.MEDIA_ROOT,
#         }),
#         url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
#             'document_root': settings.STATIC_ROOT,
#         }),
# )
