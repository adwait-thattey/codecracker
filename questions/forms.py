from django import forms
from questions.models import Question, Submission, TestCase, Category
from ckeditor.widgets import CKEditorWidget


class PostQuestionForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Select A Category", to_field_name="name")
    class Meta:
        model = Question
        fields = ['title', 'category', 'unique_code', 'short_description', 'description', 'input_format',
                  'output_format', 'sample_input', 'sample_output', 'constraints', 'time_limit', ]


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['language', 'code']


class TestCaseCreateForm(forms.ModelForm):
    class Meta:
        model = TestCase
        fields = ['input_file', 'output_file', 'points']


class QuestionsFilterForm(forms.Form):
    SORT_CHOICES = (
        ('1', 'Most Recent'),
        ('2', 'Most Submissions'),
        ('3', 'Most Viewed'),
        ('4', 'Difficulty')
    )
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Select A Category", required=False)

    sort_by = forms.ChoiceField(choices=SORT_CHOICES, widget=forms.RadioSelect())

    reverse = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    query = forms.CharField(required=False)