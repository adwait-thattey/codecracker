from django.http import JsonResponse
from django.shortcuts import render, redirect
from registration.models import *


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


def notification(request):
    ret_data = {
        "notification": []
    }

    if request.user.is_anonymous:
        return JsonResponse(ret_data)


    # blog = get_object_or_404(Blog, pk=blog_id)

    try:
        # blog.upvote(request.user)
        ret_data["notification"] = [i['content'] for i in Notifications.objects.filter(user=request.user).values("content")]
        print(ret_data)


    except:
        pass

    return JsonResponse(ret_data)
