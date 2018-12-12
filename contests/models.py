import datetime
import decimal

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, RegexValidator, MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver

from questions.models import Question, Submission

unique_code_validator = RegexValidator(r'^[0-9a-z]*$',
                                       "The Unique code can contain only small case alphabets and numbers ")


class Contest(models.Model):
    title = models.CharField(max_length=200)

    author = models.ForeignKey(to=User, on_delete=models.PROTECT)

    short_description = models.TextField(verbose_name="Short Description",
                                         max_length=250,
                                         help_text="A short description whch describes your contest.",
                                         null=True,
                                         )

    description = RichTextUploadingField(help_text="Give a brief or detailed description for your contest")

    eligibility = models.CharField(null=True, help_text="What is the eligibility criteria for participants?",
                                   max_length=200)

    rules = models.CharField(null=True, help_text="What are the rules that all participants must follow?",
                             max_length=200)

    prizes = models.CharField(null=True, help_text="Mention prizes for diff positions/winners (If any)", max_length=200)

    contacts = models.EmailField(null=True,
                                 help_text="Give your email, phone etc. so that people can contact you if they need to")

    start_date = models.DateField(verbose_name="Start Date")

    start_time = models.TimeField(verbose_name="Start Time", null=True)

    end_date = models.DateField(verbose_name="End Date")

    end_time = models.TimeField(verbose_name="End Time", null=True)

    unique_code = models.CharField(verbose_name="Unique Code",
                                   max_length=15,
                                   validators=[MinLengthValidator(3), unique_code_validator],
                                   unique=True,
                                   db_index=True,
                                   help_text="A unique code for your contest. between 3-15 characters. May contain only \
                                      lowercase characters and numbers. For example if the question name is 'Sorting Array', \
                                      you may name the code SORTARR"
                                   )

    is_public = models.BooleanField(verbose_name="Is this Public?", default=True,
                                    help_text="If you choose to make this non public, please enter a link below that participants will\
                                  click to register for the contest. It can lead to a form or a website etc. After they complete \
                                  registration, it is your responsibility to add them in the participants list via\
                                   the REST API call.")


    status = models.IntegerField(default=0, help_text="0-Yet to start, 1- live, 2- ended",
                                 validators=[MinValueValidator(0), MaxValueValidator(2)])

    registration_link = models.URLField(verbose_name="Registration Link", blank=True)

    participants = models.ManyToManyField(to=User, related_name="participating_contests")

    def __str__(self):
        return self.unique_code

class ContestQuestion(models.Model):
    question = models.OneToOneField(to=Question, on_delete=models.CASCADE)
    contest = models.ForeignKey(to=Contest, on_delete=models.PROTECT)
    points = models.IntegerField(default=0, null=False)

    def __str__(self):
        return self.question.unique_code


class ContestLiveSubmission(models.Model):
    submission = models.OneToOneField(to=Submission, on_delete=models.CASCADE)
    score = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    timedelta = models.PositiveIntegerField()

    def __str__(self):
        return str(self.id)


class ContestQuestionTopSubmission(models.Model):
    contestsubmission = models.OneToOneField(to=ContestLiveSubmission, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    contest_question = models.ForeignKey(to=ContestQuestion, on_delete=models.CASCADE)

    # The following fields are redundant, but are kept to help in fast query access

    class Meta:
        unique_together = ['user', 'contest_question']

    def __str__(self):
        return str(self.id)


class LeaderBoard(models.Model):
    contest = models.ForeignKey(to=Contest, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    total_score = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    total_time = models.PositiveIntegerField()

    class Meta:
        unique_together = ['contest', 'user']

    def __str__(self):
        return self.contest.unique_code + ":" + self.user.username


def calc_contest_submission_score(submission):
    percentage = submission.total_score
    points = submission.question.contestquestion.points

    return decimal.Decimal(points) * (decimal.Decimal(percentage) / decimal.Decimal(100.0))


def update_top_contest_submission(contestsubmission):
    contest_submission_set = ContestLiveSubmission.objects.filter(
        submission__question=contestsubmission.submission.question,
        submission__user=contestsubmission.submission.user).order_by('timedelta').order_by('-score')
    if contest_submission_set.exists():
        top_submission = ContestQuestionTopSubmission.objects.filter(user=contestsubmission.submission.user,
                                                                     contest_question=contestsubmission.submission.question.contestquestion)
        if top_submission.exists():
            top_submission = top_submission[0]
            if contest_submission_set[0].score > top_submission.contestsubmission.score:
                top_submission.contestsubmission = contest_submission_set[0]
                top_submission.save()
        else:
            ContestQuestionTopSubmission.objects.create(contestsubmission=contest_submission_set[0],
                                                        user=contest_submission_set[0].submission.user,
                                                        contest_question=contest_submission_set[
                                                            0].submission.question.contestquestion)


@receiver(post_save, sender=Submission)
def create_contest_submission(sender, instance, created, **kwargs):
    if created:
        if hasattr(instance.question, 'contestquestion'):
            if instance.question.contestquestion.contest.status == 1:
                timediff = datetime.datetime.now() - datetime.datetime.combine(
                    instance.question.contestquestion.contest.start_date,
                    instance.question.contestquestion.contest.start_time)
                ContestLiveSubmission.objects.create(submission=instance, timedelta=timediff.total_seconds())


@receiver(post_save, sender=Submission)
def update_contest_submission_points(sender, instance, **kwargs):
    if hasattr(instance, 'contestlivesubmission'):
        instance.contestlivesubmission.score = calc_contest_submission_score(instance)
        instance.contestlivesubmission.save()
        update_top_contest_submission(instance.contestlivesubmission)


@receiver(post_save, sender=ContestQuestionTopSubmission)
def update_contest_submission(sender, instance, created, **kwargs):
    L = LeaderBoard.objects.filter(user=instance.user, contest=instance.contest_question.contest)
    if created:
        if L.exists():
            L = L[0]
            L.total_score += instance.contestsubmission.score
            L.total_time += instance.contestsubmission.timedelta
            L.save()
        else:
            L = LeaderBoard.objects.create(
                user=instance.user,
                contest=instance.contest_question.contest,
                total_score=instance.contestsubmission.score,
                total_time=instance.contestsubmission.timedelta
            )

    else:
        L = L[0]
        qset = ContestQuestionTopSubmission.objects.filter(user=L.user, contest_question__contest=L.contest).aggregate(
            points=Sum('contestsubmission__score'), time=Sum('contestsubmission__timedelta'))
        L.total_score = qset['points']
        L.total_time = qset['time']
        L.save()
