from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Avg
from datetime import date
from django.utils import timezone
from dateutil.relativedelta import relativedelta


# Create your views here.
# Anybody can get anybody's stats
# There is no restriction
from questions.models import Submission


def user_submission_date_stats(request, username):
    user = get_object_or_404(User, username=username)
    all_submissions = user.submission_set.all()
    # all_submissions = Submission.objects
    submission_dates = all_submissions.values('submitted_on__date').annotate(count=Count('id')).values('submitted_on__date', 'count').order_by('submitted_on__date')

    req_stats = list()
    for S in submission_dates:
        D = {"x":S['submitted_on__date'].strftime('%m/%d/%Y'), "y":S['count']}
        req_stats.append(D)

    return JsonResponse({"stats":req_stats }, safe=False)


def user_submission_percentage(request, username):
    user = get_object_or_404(User, username=username)

    submission_set = user.submission_set
    total_submissions = submission_set.count()
    correct_submissions = submission_set.filter(total_score__gte=99).count()

    req_stats = [
         correct_submissions, total_submissions
    ]

    return JsonResponse({"stats":req_stats}, safe=False)

def user_per_question_attempts_stats(request, username):
    user = get_object_or_404(User, username=username)

    user_submissions= user.submission_set

    question_submission_count = list(user_submissions.values('question').annotate(count=Count('id')).values('question', 'count').order_by('question'))

    ret_stats = {
        "question_submission_count": question_submission_count
    }

    return JsonResponse({'stats':ret_stats}, safe=False)
def user_question_attempts_stats(request, username):
    user = get_object_or_404(User, username=username)

    submission_set = user.submission_set

    total_question_count = len(submission_set.values('question').annotate(count=Count('id')).values('question', 'count').order_by('question'))

    correct_question_count = len(submission_set.filter(total_score__gte = 99).values('question').annotate(count=Count('id')).values('question', 'count').order_by('question'))

    ret_stats = [
         correct_question_count, total_question_count
    ]

    return JsonResponse({"stats":ret_stats}, safe=False)

def user_avg_attempts_per_question(request, username):
    user = get_object_or_404(User, username=username)

    submission_set = user.submission_set

    avg = submission_set.values('question').annotate(count=Count('question')).values('question', 'count').order_by('question').aggregate(Avg('count'))

    ret_stats = {
        "avg": avg
    }

    return JsonResponse({"stats":ret_stats}, safe=False)

def chart(request):
    current = (date.today()).strftime('%d %b %Y')
    one_month = (date.today() + relativedelta(months=-1)).strftime('%d %b %Y')
    six_months = (date.today() + relativedelta(months=+6)).strftime('%d %b %Y')
    one_year = (date.today() + relativedelta(months=-12)).strftime('%d %b %Y')
    ytd = (date.today().replace(day= 1 ,month = 1)).strftime('%d %b %Y')

    print(ytd)
    return render(request, "stats/Profile_statistics.html",{'one_month':str(one_month),
            'six_months':str(six_months),
            'one_year':str(one_year),
            'current':str(current),
            'ytd':str(ytd),})

def display_pie(request):
    return render(request,"stats/Profile_statistics_pie.html")