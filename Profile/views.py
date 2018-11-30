from django.http import JsonResponse
from django.shortcuts import render, redirect

def profile_stats(request):
    return render(request,'Profile/Profile_statistics.html')


def profile_stats_pie(request):
    return render(request,'Profile/Profile_statistics_pie.html')