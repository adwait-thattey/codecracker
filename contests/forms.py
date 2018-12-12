from django import forms
from contests.models import Contest, ContestQuestion
from ckeditor.widgets import CKEditorWidget


class HostContestForm(forms.ModelForm):
    class Meta:
        model = Contest
        fields = ['title', 'unique_code','start_date','start_time','end_date', 'end_time', 'short_description', 'description', 'eligibility',
                  'rules', 'prizes', 'contacts', 'is_public', 'registration_link', ]

class ContestQuestionForm(forms.ModelForm):
    class Meta:
        model = ContestQuestion
        fields = ['points']

class ContestFilterForm(forms.Form):
    SORT_CHOICES = (
        ('1', 'Start Time'),
        ('2', 'End Time'),
        ('3', 'Status'),
    )

    STATUS_CHOICES = (
        (None, 'Status'),
        ('1', 'Live Contests'),
        ('0', 'Upcoming Contests'),
        ('2', 'Past Contests')
    )
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False)

    sort_by = forms.ChoiceField(choices=SORT_CHOICES, widget=forms.RadioSelect())

    reverse = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    # query = forms.CharField(required=False)