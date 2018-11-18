from django.shortcuts import render, redirect

# Create your views here.
from questions.models import Category


def landing_page(request):
    categories = Category.objects.all()
    return render(request, 'main_page/landing_page.html',  {"categories": categories})


def redirect_to_landing(request):
    return redirect('landing')


def home(request):
    categories = Category.objects.all()
    return render(request, 'main_page/home.html', {"categories": categories})


def redirect_to_home(request):
    return redirect('home')


def nav(request):
    return render(request, 'main_page/nav.html')
