from rest_framework import serializers
from .models import Contest,ContestQuestion


class ContestSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Contest
        fields = ('title','author','short_description','description','eligibility','rules','prizes','contacts',
                  'start_date','start_time','end_date','end_time','unique_code','is_public','registration_link',
                  'participants')


class ContestQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContestQuestion
        fields = ('question','contest','points')