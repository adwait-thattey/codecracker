from django.urls import reverse
from django_cron import CronJobBase, Schedule
from datetime import datetime
from contests.models import Contest
from registration.models import send_notification


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
                send_notification(user=c.author,
                                  content=f"Your contest {c.unique_code} has started",
                                  link=reverse("contests:view-contest",
                                               args=[c.unique_code]),
                                  icon="assistant_photo"
                                  )

                for p in c.participants.all():
                    send_notification(user=p,
                                      content=f"Your contest {c.unique_code} has started",
                                      link=reverse("contests:view-contest",
                                                   args=[c.unique_code]),
                                      icon="assistant_photo"
                                      )
        contests = Contest.objects.filter(status=1)
        for c in contests:
            if datetime.now() > datetime.combine(c.end_date, c.end_time):
                c.status = 2
                c.save()
                send_notification(user=c.author,
                                  content=f"Your contest {c.unique_code} has ended",
                                  link=reverse("contests:view-contest",
                                               args=[c.unique_code]),
                                  icon="assistant_photo"
                                  )

                for p in c.participants.all():
                    send_notification(user=p,
                                      content=f"Your contest {c.unique_code} has ended",
                                      link=reverse("contests:view-contest",
                                                   args=[c.unique_code]),
                                      icon="assistant_photo"
                                      )
