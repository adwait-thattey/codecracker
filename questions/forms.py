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


class TestCaseForm(forms.ModelForm):
    class Meta:
        model = TestCase
        fields = ['input_file', 'output_file', 'points']

    def clean(self):
        cleaned_data = super().clean()
        input_file = str(cleaned_data.get('input_file'))
        output_file = str(cleaned_data.get('output_file'))

        if not input_file or input_file=="None":
            self.add_error('input_file', 'This field is required')

        if not output_file or output_file=="None":
            self.add_error('output_file', 'This field is required')
