from django_cron import CronJobBase, Schedule
from datetime import datetime
from contests.models import Contest


class ContestStatus(CronJobBase):

    RUN_EVERY_MINS = 1
    RETRY_AFTER_FAILURE_MINS = 2
    MIN_NUM_FAILURES = 5
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS, retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'contests.cron'

    def do(self):
        contests = Contest.objects.filter(status=0)
        for c in contests:
            if datetime.now() > datetime.combine(c.start_date, c.start_time):
                c.status = 1
                c.save()

        contests = Contest.objects.filter(status=1)
        for c in contests:
            if datetime.now() > datetime.combine(c.end_date, c.end_time):
                c.status = 2
                c.save()
