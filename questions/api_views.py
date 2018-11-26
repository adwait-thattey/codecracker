from django.http import Http404

from questions.models import Question
from .serializers import QuestionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class QuestionDetail(APIView):

    def get_question(self, unique_code):
        try:
            return Question.objects.get(unique_code=unique_code)
        except Question.DoesNotExist:
            raise Http404

    def get(self, request, unique_code, format=None):
        question = self.get_question(unique_code)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    def put(self, request, unique_code, format=None):
        question = self.get_question(unique_code)
        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)

    def delete(self, request, unique_code, format=None):
        question = self.get_question(unique_code)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
