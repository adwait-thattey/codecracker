from django.urls import path
from . import api_views

urlpatterns = [
    path('<slug:unique_code>/view', api_views.QuestionDetail.as_view()),
    path('<slug:unique_code>/test-case/create', api_views.TestCaseCreateView.as_view()),
    path('<slug:unique_code>/test-case/<int:number>/view', api_views.TestCaseViewUpdateView.as_view()),
]