from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
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
    submission_dates = all_submissions.values('submitted_on__date').annotate(count=Count('id')).values('submitted_on__date', 'count')

    req_stats = list()
    if submission_dates:

        cur_date = submission_dates[0]['submitted_on__date']
        cur_count = 0
        for S in submission_dates:
            if S['submitted_on__date']==cur_date:
                cur_count+=S['count']
            else:
                D = {"x":cur_date.strftime('%m/%d/%Y'), "y":cur_count}
                req_stats.append(D)
                cur_date = S['submitted_on__date']
                cur_count = S['count']



    return JsonResponse({"stats":req_stats }, safe=False)


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