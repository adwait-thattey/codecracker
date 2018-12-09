from django.contrib import admin

# Register your models here.
from contests.models import Contest, ContestQuestion, ContestLiveSubmission, ContestQuestionTopSubmission, LeaderBoard

admin.site.register(Contest)


class ContestQuestionAdmin(admin.ModelAdmin):
    list_display = ['question', 'contest', 'points']


admin.site.register(ContestQuestion, ContestQuestionAdmin)


class ContestLiveSubmissionAdmin(admin.ModelAdmin):
    def user(self, obj):
        return obj.submission.user.username

    def question(self, obj):
        return obj.submission.question.unique_code

    def contest(self, obj):
        return obj.submission.question.contestquestion.contest.unique_code

    list_display = ['user', 'contest', 'question', 'score', 'timedelta']
    list_filter = ['submission__question__contestquestion__contest', 'submission__user', 'submission__question']


admin.site.register(ContestLiveSubmission, ContestLiveSubmissionAdmin)


class ContestQuestionTopSubmissionAdmin(admin.ModelAdmin):
    def score(self, obj):
        return obj.contestsubmission.score

    def timedelta(self, obj):
        return obj.contestsubmission.timedelta

    list_display = ['user', 'contest_question', 'score', 'timedelta']
    list_filter = ['user', 'contest_question']


admin.site.register(ContestQuestionTopSubmission, ContestQuestionTopSubmissionAdmin)


class LeaderBoardAdmin(admin.ModelAdmin):
    list_display = ['user', 'contest', 'total_score', 'total_time']
    sortable_by = ['user', 'contest', 'total_score', 'total_time']
    list_filter = ['contest__unique_code', 'user']


admin.site.register(LeaderBoard, LeaderBoardAdmin)
