from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Count

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
                D = {"x":cur_date.strftime('%d/%m/%Y'), "y":cur_count}
                req_stats.append(D)
                cur_date = S['submitted_on__date']
                cur_count = S['count']



    return JsonResponse(req_stats, safe=False)