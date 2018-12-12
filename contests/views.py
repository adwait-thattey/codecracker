
from time import sleep

from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from contests.models import Contest, ContestQuestion, LeaderBoard
from questions.models import Question
from .forms import HostContestForm, ContestQuestionForm, ContestFilterForm
from questions.forms import PostQuestionForm
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from registration.views import email_confirmation_required

from datetime import datetime
from datetime import timedelta
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here.
@login_required
@email_confirmation_required
def contest_question_create(request, contest_unique_id=None):
    contest_id = get_object_or_404(Contest, unique_code=contest_unique_id)
    if (contest_id.author != request.user):
        return PermissionDenied("You can not post question in this contest!")
    if (request.method == "POST"):
        form = PostQuestionForm(request.POST)
        contest_question_points = ContestQuestionForm(request.POST)
        if form.is_valid() and contest_question_points.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.active = False
            question.save()
            contest_question = contest_question_points.save(commit=False)
            contest_question.contest = contest_id
            contest_question.question = question
            contest_question.save()
            return redirect('questions:view_the_question', question.unique_code)
    else:
        form = PostQuestionForm()
        contest_question_points = ContestQuestionForm()
    context = {
        'form': form,
        'cq': contest_question_points,
    }
    return render(request, 'contests/create_contest_question.html', context)



@login_required
@email_confirmation_required
def contest_question_edit(request, contest_unique_id, question_unique_id):
    question_instance = get_object_or_404(Question, unique_code=question_unique_id)
    contest_instance = get_object_or_404(Contest, unique_code=contest_unique_id)
    instance = get_object_or_404(ContestQuestion, question=question_instance, contest=contest_instance)
    form = PostQuestionForm(request.POST or None, instance=question_instance,
                            initial={"category": question_instance.category})
    contest_question_points = ContestQuestionForm(request.POST or None, instance=instance)
    if form.is_valid() and contest_question_points.is_valid():
        points = contest_question_points.cleaned_data["points"]
        contest_question_form = form.save(commit=False)
        contest_question_form.save()
        contest_question_points.save()
        return redirect('questions:view_the_question', question.unique_code)
    context = {
        'form': form,
        'cq': contest_question_points
    }
    return render(request, "contests/create_contest_question.html", context)


@login_required
@email_confirmation_required
def create_contest(request):
    if (request.method == "POST"):
        form = HostContestForm(request.POST)
        if form.is_valid():
            contest = form.save(commit=False)
            contest.author = request.user
            contest.save()
            return redirect('contests:view-contest', contest.unique_code)
        else:
            print(form.errors)
    else:
        form = HostContestForm()
    return render(request, 'contests/create_contest.html', {'form':form})

@login_required
@email_confirmation_required
def edit_contest(request, contest_unique_id):
    instance = get_object_or_404(Contest, unique_code=contest_unique_id)
    if instance.author != request.user:
        return PermissionDenied("You can not edit this question!")
    form = HostContestForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect('contests:view-contest', instance.unique_code)
    context = {
        'instance': instance,
        'form': form
    }
    return render(request, "contests/create_contest.html", context)


def view_contest_page(request, contest_unique_code):
    contest = get_object_or_404(Contest, unique_code=contest_unique_code)
    questions = ContestQuestion.objects.filter(contest__unique_code=contest_unique_code)
    C= Contest.objects.get(unique_code=contest_unique_code)
    sdt = datetime.combine(C.start_date, C.start_time) + timedelta(minutes=1)
    starttime = sdt.strftime("%d %B %Y %H:%M:%S")
    edt = datetime.combine(C.end_date, C.end_time)
    endtime = edt.strftime("%d %B %Y %H:%M:%S")
    return render(request, 'contests/contest_page.html',
                   {'contest': contest, 'questions': questions, "starttime": starttime, 'endtime': endtime})



def leaderboard(request, contest_unique_code):
    contest = get_object_or_404(Contest, unique_code=contest_unique_code)

    leaderboard = LeaderBoard.objects.filter(contest=contest).order_by('total_time').order_by('-total_score')

    return render(request, 'contests/leaderboard.html', {"leaderboard": leaderboard})


def browse_contests(request):
    contests = Contest.objects.all()

    page = request.GET.get('page', 1)
    contest_filter_form = ContestFilterForm(request.GET)

    contest_filter_form.is_valid()
    # Just did this to make sure clean is called

    if "status" in contest_filter_form.cleaned_data:
        if contest_filter_form.cleaned_data["status"]:
            contests = contests.filter(status=contest_filter_form.cleaned_data["status"])
    if "sort_by" in contest_filter_form.cleaned_data:
        # print("sortby",question_filter_form.cleaned_data["sort_by"])
        sort_by_dict = {
            "1": "-start_date",
            "2": "-end_date",
            "3": "status",
        }
        contests = contests.order_by(sort_by_dict[contest_filter_form.cleaned_data["sort_by"]])
    # if "query" in question_filter_form.cleaned_data:
    #     if question_filter_form.cleaned_data["query"] != 'None':
    #         # print("query", question_filter_form.cleaned_data["query"])
    #         questions = questions.filter(title__contains=question_filter_form.cleaned_data["query"])
    if "reverse" in contest_filter_form.cleaned_data:
        # print(contest_filter_form.cleaned_data["reverse"])
        if contest_filter_form.cleaned_data["reverse"]:
            contests = contests.reverse()

    paginator = Paginator(contests, 7)
    try:
        sleep(1.5)
        contests_page = paginator.page(page)
    except PageNotAnInteger:
        contests_page = paginator.page(1)
    except EmptyPage:
        contests_page = paginator.page(paginator.num_pages)
    # print(question_page)
    return render(request, "contests/browse_contests.html",
                  {"contests": contests_page, "filter_form": contest_filter_form})


def participants(request, contest_unique_id):
    contest = get_object_or_404(Contest,unique_code=contest_unique_id)
    participants = contest.participants.all()

    return render(request,"contests/p1.html",{'d1':participants})

@login_required
@email_confirmation_required
def register_for_contest(request, contest_unique_id):
    contest = get_object_or_404(Contest, unique_code=contest_unique_id)
    if request.user not in contest.participants.all():
        contest.participants.add(request.user)

    return redirect('contests:view-contest', contest_unique_id)

@login_required
@email_confirmation_required
def unregister_from_contest(request, contest_unique_id):
    contest = get_object_or_404(Contest, unique_code=contest_unique_id)
    if request.user in contest.participants.all():
        contest.participants.remove(request.user)

    return redirect('contests:view-contest', contest_unique_id)
