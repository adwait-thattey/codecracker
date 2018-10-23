from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, RegexValidator, FileExtensionValidator, MaxValueValidator, \
    MinValueValidator
from django.db import models
from django.contrib.auth.models import User as DefaultUser
import os


def image_upload_url(instance, filename):
    return os.path.join("catgories", str(instance.id), "logo", filename)


# Create your models here.
class Catagory(models.Model):
    name = models.CharField(max_length=25,
                            unique=True
                            )

    logo = models.ImageField(upload_to=image_upload_url,
                             blank=True,
                             null=True
                             )

    description = models.TextField()

    def __str__(self):
        return self.name


unique_code_validator = RegexValidator(r'^[0-9a-z]*$',
                                       "The Unique code can contain only small case alphabets and numbers ")


class Question(models.Model):
    author = models.ForeignKey(verbose_name="Question Poster",
                               to=DefaultUser,
                               null=True,
                               on_delete=models.SET_NULL
                               )

    title = models.CharField(verbose_name="Title",
                             max_length=80
                             )

    description = models.TextField(verbose_name="Description")

    catagory = models.ManyToManyField(verbose_name="Catagories",
                                      to=Catagory,
                                      blank=True
                                      )

    time_limit = models.DurationField(verbose_name="Time Limit",
                                      help_text="This is approx the time limit that will be required to run a python code \
                                      for the problem. This limit will be automatically reduced for other languages \
                                      like C which take much lesser time for similar implementation"
                                      )

    unique_code = models.CharField(verbose_name="Unique Code",
                                   max_length=15,
                                   validators=[MinLengthValidator(3), unique_code_validator],
                                   unique=True,
                                   help_text="A unique code for your question. between 3-15 characters. May contain only \
                                   lowercase characters and numbers. For example if the question name is 'Sorting Array', \
                                   you may name the code SORTARR")

    def __str__(self):
        return self.unique_code


def get_testcase_input_upload_path(instance, filename):
    return os.path.join("questions", str(instance.question.unique_code), "testcases", str(instance.id), "input.txt")


def get_testcase_output_upload_path(instance, filename):
    return os.path.join("questions", str(instance.question.unique_code), "testcases", str(instance.id), "output.txt")


class TestCase(models.Model):
    question = models.ForeignKey(verbose_name="Question",
                                 to=Question,
                                 on_delete=models.CASCADE
                                 )

    input = models.FileField(verbose_name="File Containing Input",
                             upload_to=get_testcase_input_upload_path,
                             validators=[FileExtensionValidator(['txt'],
                                                                message="Only text files are allowed as input and outpur")],
                             )

    output = models.FileField(verbose_name="File Containing Expected Input",
                              upload_to=get_testcase_output_upload_path,
                              validators=[FileExtensionValidator(['txt'],
                                                                 message="Only text files are allowed as input and output")],
                              )

    points = models.PositiveIntegerField(verbose_name="Points",
                                         help_text="The number of points that user will get if he/she completes this \
                                         test case successfully. The total points lateron will be calculated as a percentage of 100")


def get_code_upload_url(instance, filename):
    return os.path.join("users", str(instance.user.id), "submissions", str(instance.question.unique_code), filename)


class Submission(models.Model):
    ALLOWED_LANGUAGES = (
        ('PY', "Python2"),
        ('PY3', "Python3")
    )

    question = models.ForeignKey(to=Question,
                                 on_delete=models.CASCADE
                                 )

    user = models.ForeignKey(to=DefaultUser,
                             on_delete=models.CASCADE
                             )

    language = models.CharField(max_length=5,
                                choices=ALLOWED_LANGUAGES
                                )

    code = models.FileField(upload_to=get_code_upload_url)

    total_score = models.FloatField(default=0, editable=False, validators=[MinValueValidator(0.0, "The score can not be negative"), MaxValueValidator(100.0, "Total Score must be calculated as a percentage of 100")])

    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    def clean(self):
        super().clean()

        # Validate File name extensions based on language of choice
        extension_dict = {
            "PY": ".py",
            "PY3": ".py"
        }

        code_filename, code_fileextension = os.path.splitext(str(self.code))
        print(code_fileextension)
        if code_fileextension.lower() != extension_dict[self.language]:
            raise ValidationError("Please choose a valid file corresponding to the language chosen ")


class Result(models.Model):
    testcase = models.ForeignKey(to=TestCase, on_delete=models.CASCADE)
    submission = models.ForeignKey(to=Submission, on_delete=models.CASCADE)
    pass_fail = models.BooleanField(default=False,
                                    help_text="False means code did not pass the TC.True means it passes",
                                    editable=False
                                    )
