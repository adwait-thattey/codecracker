from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from contests.models import Contest, ContestQuestion
from questions.models import Question
from .forms import HostContestForm, ContestQuestionForm
from questions.forms import PostQuestionForm
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def contest_question_create(request, contest_unique_id=None):
    c_id = get_object_or_404(Contest, unique_code=contest_unique_id)
    if (c_id.author != request.user):
        return PermissionDenied("You can not post question in this contest!")
    if (request.method == "POST"):
        form = PostQuestionForm(request.POST)
        cq= ContestQuestionForm(request.POST)
        if form.is_valid() and cq.is_valid():
            points= cq.cleaned_data["points"]
            cq_form = form.save()
            cq.author = request.user
            cq.active = False
            cq.save()
            CQ=ContestQuestion.objects.create(question=cq_form, contest=c_id, points=points)
            CQ.save()
            return HttpResponse("Successfully added question in contest!!!")
    else:
        form = PostQuestionForm()
        cq= ContestQuestionForm()
    context = {
        'form':form,
        'cq':cq,
    }
    return render(request, 'contests/create_contest_question.html', context)



def contest_question_edit(request, contest_unique_id, question_unique_id):
    instance1=get_object_or_404(Question, unique_code=question_unique_id)
    instance2=get_object_or_404(Contest, unique_code=contest_unique_id)
    instance = get_object_or_404(ContestQuestion, question=instance1, contest=instance2)
    form = PostQuestionForm(request.POST or None, instance=instance1, initial={"category":instance1.category})
    cq= ContestQuestionForm(request.POST or None, instance=instance)
    if form.is_valid() and cq.is_valid():
        points= cq.cleaned_data["points"]
        cq_form = form.save(commit=False)
        #CQ=ContestQuestion.objects.create(question=cq_form, contest=instance2, points=points)
        #CQ.save()
        cq_form.save()
        cq.save()
        return HttpResponse("Successfully edited question in contest!!!")
    context = {
    'form': form,
    'cq': cq
    }
    return render(request, "contests/create_contest_question.html", context)

def create_contest(request):
    if (request.method == "POST"):
        form = HostContestForm(request.POST)
        if form.is_valid():
            contest = form.save(commit=False)
            contest.author = request.user
            contest.save()
            return HttpResponse('contest saved!!')
        else:
            print(form.errors)
    else:
        form = HostContestForm()
    return render(request, 'contests/create_contest.html', {'form':form})


def edit_contest(request, contest_unique_id):
    instance = get_object_or_404(Contest, unique_code=contest_unique_id)
    if instance.author != request.user:
        return PermissionDenied("You can not edit this question!")
    form = HostContestForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponse("edited!!")
    context = {
        'instance': instance,
        'form': form
    }
    return render(request, "contests/create_contest.html", context)
