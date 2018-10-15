from django.db import models
from django.contrib.auth.models import User as DefaultUser
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.db.models import signals


# Create your models here.

class Institute(models.Model):
    name = models.CharField(verbose_name="Name Of Institute", max_length=50)


def phone_number_validator(phone_number):
    try:
        phone_number = str(phone_number)
    except ValueError:
        raise ValidationError("Invalid Input")

    if phone_number.isdigit() is False:
        raise ValidationError("Phone Number can contain only numbers ")

    if not 10 <= len(phone_number) <= 11:
        raise ValidationError("Length of phone number must be either 10 or 11")


class MoreUserData(models.Model):
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
                                  on_delete=models.PROTECT
                                  )

    designation = models.CharField(verbose_name="Designation Of User",
                                   max_length=5,
                                   choices=DESIGNATION_CHOICES,
                                   default="STU"
                                   )


class GoogleAuth(models.Model):
    user = models.OneToOneField(to=DefaultUser,
                                on_delete=models.CASCADE
                                )

    google_id = models.CharField(max_length=250)

    salt = models.CharField(max_length=250)


class EmailConfirmation(models.Model):
    user = models.OneToOneField(to=DefaultUser,
                                on_delete=models.CASCADE
                                )

    email_confirmed = models.BooleanField(default=False)


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
