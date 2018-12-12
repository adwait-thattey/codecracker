from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser

from questions.models import Question, TestCase
from .serializers import QuestionSerializer, TestCaseSerializer
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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, unique_code, format=None):
        question = self.get_question(unique_code)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TestCaseCreateView(APIView):
    parser_classes = (MultiPartParser,)

    def get_question(self, unique_code):
        try:
            return Question.objects.get(unique_code=unique_code)
        except Question.DoesNotExist:
            raise Http404

    def post(self, request, unique_code):
        question = self.get_question(unique_code)
        print(request.data)
        serializer = TestCaseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(question=question, number=question.testcase_set.count() + 1)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TestCaseViewUpdateView(APIView):
    parser_classes = (MultiPartParser,)

    def get_question(self, unique_code):
        try:
            return Question.objects.get(unique_code=unique_code)
        except Question.DoesNotExist:
            raise Http404

    def get(self, request, unique_code, number, format=None):
        test_case = get_object_or_404(TestCase, question__unique_code=unique_code, number=number)
        test_case_serializer = TestCaseSerializer(test_case)

        return Response(test_case_serializer.data)

    def post(self, request, unique_code, number, format=None):
        test_case = get_object_or_404(TestCase, question__unique_code=unique_code, number=number)
        serializer = TestCaseSerializer(test_case, request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


