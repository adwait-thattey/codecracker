from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from registration.models import *

# Create your views here.
from questions.models import Category
from contests.models import Contest
from registration.views import email_confirmation_required


def landing_page(request):
    categories = Category.objects.all()
    return render(request, 'main_page/landing.html', {"categories": categories})


def redirect_to_landing(request):
    return redirect('landing')


def home(request):
    categories = Category.objects.all()
    contest = Contest.objects.all()
    coming_contests= contest[:4]
    context={
        'categories': categories,
        'coming_contests': coming_contests,
    }
    return render(request, 'main_page/home.html', context)


def redirect_to_home(request):
    return redirect('home')


def nav(request):
    return render(request, 'main_page/nav.html')


@login_required
@email_confirmation_required
def get_all_notifications(request):
    ret_data = {"notifications": list(Notification.objects.filter(user=request.user).values_list('content', 'icon', 'link'))}
    # print(ret_data)

    return JsonResponse(ret_data)

@login_required
@email_confirmation_required
def get_unseen_notifications(request):
    qset = Notification.objects.filter(user=request.user, seen=False)
    ret_data = {"notifications": list(qset.values_list('content', 'icon', 'link'))}
    # print(ret_data)

    for notif in qset :
        notif.seen = True;
        notif.save()
    return JsonResponse(ret_data)

def error_404(request):
    return render(request, "main_page/404.html")

def error_500(request):
    return render(request, "main_page/500.html")
