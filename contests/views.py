from django.shortcuts import render, get_object_or_404
from .models import Contest

# Create your views here.

def contest_question_create(contest_unique_code):
    pass

def contest_question_edit(contest_unique_code, question_unique_code):
    pass


def create_contest(request):
    return None


def edit_contest(request):
    return None

def view_contest_page(request, contest_unique_code):
	contest = get_object_or_404(Contest, unique_code= contest_unique_code)
	return render(request, 'contest_page.html', {'contest': contest})