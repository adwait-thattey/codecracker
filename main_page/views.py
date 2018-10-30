from django.shortcuts import render, redirect


# Create your views here.

def landing_page(request):
    return render(request, 'main_page/landing_page.html')


def redirect_to_landing(request):
    return redirect('landing')


def home(request):
    return render(request, 'main_page/home.html')


def redirect_to_home(request):
    return redirect('home')

def nav(request):
    return render(request, 'main_page/nav.html')
