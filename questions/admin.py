from django.contrib import admin
from .models import Category, Question, Submission, TestCase, Result


# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'q_count']
    sortable_by = ['q_count', 'name']
    search_fields = ['name']


admin.site.register(Category, CategoryAdmin)


class QuestionAdmin(admin.ModelAdmin):

    def authorusername(self, obj):
        return obj.author.username

    list_display = ['title', 'unique_code', 'authorusername', 'time_limit',
                     'input_format', 'constraints', 'output_format', 'sample_input', 'sample_output']
    sortable_by = ['time_limit', 'title']
    search_fields = ['title', 'author__username', 'unique_code']


admin.site.register(Question, QuestionAdmin)


class SubmissionAdmin(admin.ModelAdmin):
    date_hierarchy = 'submitted_on'
    list_display = ['id', 'question', 'user', 'language', 'total_score', 'submitted_on', 'last_updated']
    list_filter = ['question__unique_code', 'user__username', 'language']
    sortable_by = ['id', 'question', 'user', 'language', 'total_score', 'submitted_on', 'last_updated']
    search_fields = ['id', 'question__title', 'question__unique_code', 'language']


admin.site.register(Submission, SubmissionAdmin)


class TestCaseAdmin(admin.ModelAdmin):

    def questionname(self, obj):
        return obj.question.title

    def questioncode(self, obj):
        return obj.question.unique_code

    list_display = ['id', 'questionname', 'questioncode', 'number', 'points']
    list_filter = ['question__title', 'question__unique_code']
    sortable_by = ['id', 'question__title', 'question__unique_code', 'number', 'points']
    search_fields = ['id', 'question__title', 'number', 'question__unique_code']


admin.site.register(TestCase, TestCaseAdmin)

result_status_dict = Result.ret_status_dict()


class ResultStatusListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Result Status'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        ret_list = list()
        for key in result_status_dict:
            ret_list.append((str(key), str(result_status_dict[key])))

        return tuple(ret_list)

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        result_status_keys = [str(i) for i in list(result_status_dict.keys())]
        if self.value() in result_status_keys:
            return queryset.filter(pass_fail=int(self.value()))


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

    list_display = ['id', 'username', 'questionname', 'questionid', 'submissionid', 'result_status']
    list_filter = ['submission__user__username', 'submission__question__unique_code', 'submission__question__title',
                   ResultStatusListFilter, 'submission']
    sortable_by = ['id', 'username', 'questionname', 'questionid', 'result_status']
    search_fields = ['submission__user__username', 'submission__question__unique_code', 'submission__question__title']


admin.site.register(Result, ResultAdmin)
