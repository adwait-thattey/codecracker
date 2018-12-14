from django.db import models
from django.contrib.auth.models import User as DefaultUser
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.db.models import signals
from django.urls import reverse
from django.utils import timezone
import os


# from django.db import models


# Create your models here.

class Institute(models.Model):
    name = models.CharField(verbose_name="Name Of Institute", max_length=50)

    def __str__(self):
        return self.name


def phone_number_validator(phone_number):
    try:
        phone_number = str(phone_number)
    except ValueError:
        raise ValidationError("Invalid Input")

    if phone_number.isdigit() is False:
        raise ValidationError("Phone Number can contain only numbers ")

    if not 10 <= len(phone_number) <= 11:
        raise ValidationError("Length of phone number must be either 10 or 11")

def get_profile_picture_upload_path(instance, filename):
    return os.path.join('profiles', instance.user.username, 'profile_pic' + filename)

class UserProfile(models.Model):
    DESIGNATION_CHOICES = (
        ('STU', 'Student'),
        ('PROF', 'Professor'),
        ('TA', 'Teaching Assistant')
    )

    user = models.OneToOneField(to=DefaultUser,
                                primary_key=True,
                                on_delete=models.CASCADE
                                )

    phone_number = models.CharField(verbose_name="Phone Number",
                                    max_length=11,
                                    blank=True,
                                    validators=[phone_number_validator]
                                    )

    institute = models.ForeignKey(to=Institute,
                                  on_delete=models.PROTECT,
                                  blank=True,
                                  null=True,
                                  )

    designation = models.CharField(verbose_name="Designation Of User",
                                   max_length=5,
                                   choices=DESIGNATION_CHOICES,
                                   default="STU"
                                   )

    picture = models.ImageField(upload_to=get_profile_picture_upload_path, default="/profiles/default.png")

    about = models.TextField(verbose_name="About User", max_length=500, null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name() + "<" + self.user.username + ">"


class GoogleAuth(models.Model):
    user = models.OneToOneField(to=DefaultUser,
                                on_delete=models.CASCADE,
                                primary_key=True
                                )

    google_id = models.CharField(max_length=250, null=True, blank=True, unique=True)

    salt = models.CharField(max_length=250, null=True, blank=True, unique=True)

    def __str__(self):
        return self.user.get_full_name() + "<" + self.user.username + ">"


class EmailConfirmation(models.Model):
    user = models.OneToOneField(to=DefaultUser,
                                on_delete=models.CASCADE,
                                primary_key=True
                                )

    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.get_full_name() + "<" + self.user.username + ">"


@receiver(signals.post_save, sender=DefaultUser)
def set_email_confirmed_false(sender, instance, created, **kwargs):
    if created:
        EmailConfirmation.objects.create(user=instance)

        # Users passsing via oauth don't need to confirm email
        if instance.has_usable_password() is False:
            instance.emailconfirmation.email_confirmed = True

        # Superusers don't need to confirm emails
        elif instance.is_superuser:
            instance.emailconfirmation.email_confirmed = True

        instance.emailconfirmation.save()


@receiver(signals.post_save, sender=DefaultUser)
def create_profile_and_oauth(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        GoogleAuth.objects.create(user=instance)


class Notification(models.Model):
    user = models.ForeignKey(verbose_name="User",
                             to=DefaultUser,
                             on_delete=models.SET_NULL,
                             null=True,
                             )

    content = models.TextField(verbose_name="content",
                               max_length=250,
                               help_text="Notification content",
                               )

    icon = models.CharField(verbose_name="icon",
                            max_length=50,

                            )

    link = models.CharField(verbose_name="link", help_text="USE ONLY NAME. NOT FULL TEXT", max_length=200)
    seen = models.BooleanField(default=False)
    time_stamp = models.DateTimeField(verbose_name="time_stamp",
                                      auto_now_add=True)

    def __str__(self):
        return self.user.get_full_name() + "<" + self.user.username + ">"

    class Meta:
        ordering = ['-time_stamp']


def send_notification(user=None, username=None, content="", icon="", link=""):
    if user == None:
        if username == None:
            print("ERROR: You must provide either user or username")
        else:
            user = DefaultUser.objects.filter(username=username)
            if user.exists() is False:
                print("ERROR: User with given username does not exist")
            else:
                user = user[0]

    Notification.objects.create(user=user, content=content, icon=icon, link=link)
