from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django_cron import CronJobBase, Schedule
from datetime import datetime
from .models import Contest


class ContestStatus(self):
    def __super__(CronJobBase):
        pass

    def __init__(self, unique_code):
        self.unique_code = unique_code

    RUN_EVERY_MINS = 1
    RETRY_AFTER_FAILURE_MINS = 2
    ALLOW_PARALLEL_RUNS = True
    MIN_NUM_FAILURES = 5
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS, retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'contests.cron'
    startdate = Contest.objects.get(unique_code=self.unique_code).start_date
    starttime = Contest.objects.get(unique_code=self.unique_code).start_time
    enddate = Contest.objects.get(unique_code=self.unique_code).start_date
    endtime = Contest.objects.get(unique_code=self.unique_code).start_date
    isactive = Contest.objects.get(unique_code=self.unique_code).is_active

    def do(self):
        dt = datetime.now()
        if datetime.now() > dt.combine(startdate, starttime):
            status = 0
            isactive = False
            isactive.save()

        elif datetime.now() < dt.combine(startdate, starttime) and datetime.now() > dt.combine(enddate, endtime):
            status = 1
            isactive = True
            isactive.save()

        else:
            status = -1
            isactive = False
            isactive.save()
            isactive = Contest.objects.get(unique_code=self.unique_code).is_active

        return render(request, 'contests/contest_page.html',
                      {'contest': contest, "starttime": starttime, 'status': status})
