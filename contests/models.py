from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models

# Create your models here.
from questions.models import Question

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

    eligibility = models.CharField(null=True, help_text="What is the eligibility criteria for participants?", max_length=200)

    rules = models.CharField(null=True, help_text="What are the rules that all participants must follow?", max_length=200)

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

    is_active = models.BooleanField(default=True)

    registration_link = models.URLField(verbose_name="Registration Link", blank=True)

    participants = models.ManyToManyField(to=User, related_name="participating_contests")

class ContestQuestion(models.Model):
    question = models.OneToOneField(to=Question, on_delete=models.CASCADE)
    contest = models.ForeignKey(to=Contest, on_delete=models.PROTECT)
    points = models.IntegerField(default=0, null=False)
