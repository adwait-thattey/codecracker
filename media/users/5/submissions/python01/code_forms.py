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
