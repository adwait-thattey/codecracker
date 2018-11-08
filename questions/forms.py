from django import forms

from questions.models import Question, Submission, TestCase


class PostQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'short_description', 'description', 'time_limit', 'unique_code']


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['language', 'code']


class TestCaseCreateForm(forms.ModelForm):

    class Meta:
        model = TestCase
        fields = ['input_file', 'output_file', 'points']


