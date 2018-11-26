from rest_framework import serializers
from .models import Question, Category

class QuestionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Question
		fields = ( 'unique_code', 'title', 'author', 'active', 'short_description', 'description', 'input_format',
				 'constraints', 'output_format', 'sample_input', 'sample_output', 'difficulty', 'category', 'time_limit',
				 'view_count', 'submission_count', 'create_timestamp', 'last_updated' )