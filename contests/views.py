from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.core.exceptions import PermissionDenied
from contests.models import Contest

# Create your views here.

def contest_question_create(contest_unique_code):
    pass

def contest_question_edit(contest_unique_code, question_unique_code):
    pass


def create_contest(request):
    return None


def edit_contest(request):
    return None
def participants(request, contest_unique_id):
	contest = get_object_or_404(Contest,unique_code=contest_unique_id)
	participants = contest.participants.all()

	return render(request,"contests/p1.html",{'d1':participants})




	  
