from django.contrib import admin
from .models import Catagory, Question, Submission, TestCase, Result


# Register your models here.

class CatagoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'q_count']
    sortable_by = ['q_count', 'name']
    search_fields = ['name']


admin.site.register(Catagory, CatagoryAdmin)


class QuestionAdmin(admin.ModelAdmin):

    def authorusername(self, obj):
        return obj.author.username

    list_display = ['title', 'unique_code', 'authorusername', 'time_limit']
    sortable_by = ['time_limit', 'title']
    search_fields = ['title', 'author__username', 'unique_code']


admin.site.register(Question, QuestionAdmin)


class SubmissionAdmin(admin.ModelAdmin):
    date_hierarchy = 'time_stamp'
    list_display = ['id','question', 'user', 'language', 'total_score', 'time_stamp']
    list_filter = ['question__unique_code', 'user__username', 'language']
    sortable_by = ['id', 'question', 'user', 'language', 'total_score', 'time_stamp']
    search_fields = ['id','question__title', 'question__unique_code', 'language']


admin.site.register(Submission, SubmissionAdmin)


class TestCaseAdmin(admin.ModelAdmin):

    def questionname(self, obj):
        return obj.question.title

    def questioncode(self, obj):
        return obj.question.unique_code

    list_display = ['id', 'questionname', 'questioncode','number', 'points']
    list_filter = ['question__title', 'question__unique_code']
    sortable_by = ['id', 'question__title', 'question__unique_code','number', 'points']
    search_fields = ['id', 'question__title', 'number','question__unique_code']


admin.site.register(TestCase, TestCaseAdmin)


class ResultAdmin(admin.ModelAdmin):

    def questionname(self, obj):
        return obj.submission.question.title

    def questioncode(self, obj):
        return obj.submission.unique_code

    def username(self, obj):
        return obj.submission.user.username

    def questionid(self, obj):
        return obj.submission.question.id

    def submissionid(self, obj):
        return obj.submission.id

    list_display = ['id', 'username', 'questionname', 'questionid', 'submissionid', 'pass_fail']
    list_filter = ['submission__user__username', 'submission__question__unique_code', 'submission__question__title',
                   'pass_fail']
    sortable_by = ['id', 'username', 'questionname', 'questionid', 'pass_fail']
    search_fields = ['submission__user__username', 'submission__question__unique_code', 'submission__question__title']


admin.site.register(Result, ResultAdmin)
