from django.urls import path
from . import api_views

urlpatterns = [
    path('<slug:unique_code>', api_views.QuestionDetail.as_view())
]