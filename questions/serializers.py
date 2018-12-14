from rest_framework import serializers
from .models import Question, Category, TestCase,Result


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('unique_code', 'title', 'author', 'active', 'short_description', 'description', 'input_format',
                   'constraints', 'output_format', 'sample_input', 'sample_output', 'difficulty', 'category', 'time_limit',
                   'view_count', 'submission_count', 'create_timestamp', 'last_updated')


class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = ('input_file', 'output_file', 'points')


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ('testcase', 'submission', 'pass_fail', 'errors')