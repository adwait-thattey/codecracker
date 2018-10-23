from django.contrib import admin
from .models import Catagory, Question, Submission

# Register your models here.

admin.site.register(Catagory)
admin.site.register(Question)

class SubmissionAdmin(admin.ModelAdmin):
    date_hierarchy = 'time_stamp'
    list_display = ['question', 'user', 'language', 'total_score', 'time_stamp']
    list_filter = ['question__unique_code', 'user__username', 'language']
    sortable_by = ['question', 'user', 'language', 'total_score', 'time_stamp']
    search_fields = ['question__title', 'question__unique_code', 'language']

admin.site.register(Submission, SubmissionAdmin)
