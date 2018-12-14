from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser
from rest_framework.renderers import JSONRenderer
from questions.models import Question, TestCase, Result
from .serializers import QuestionSerializer, TestCaseSerializer, ResultSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class ResultDetail(APIView):

    def get_result(self, question_unique_id):
        try:
            return Result.objects.get(question__unique_code=question_unique_id)
        except Question.DoesNotExist:
            raise Http404

    def get(self, request, question_unique_id, format=None):
        result = self.get_result(question_unique_id)
        serializer = ResultSerializer(result)
        return Response(serializer.data)


class QuestionCreate(APIView):
    """
    Create a question
    """
    def post(self, request, format=None):

        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuestionDetail(APIView):
    """
    Create , View , Update , Questions

    get:
    Get details of a question with unique code

    put:
    Add a new question or update existing

    delete:
    Delete existing question
    """
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
        if request.user != question.author:
            return JsonResponse({"error":"You are not allowed to edit this question"})
        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, unique_code, format=None):
        question = self.get_question(unique_code)
        if request.user != question.author:
            return JsonResponse({"error":"You are not allowed to delete this question"})
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
        if request.user != question.author:
            return JsonResponse({"error":"You are not allowed to add testcases to this question"})

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
        if request.user != test_case.question.author:
            return JsonResponse({"error":"You are not allowed to view this test case details"})
        test_case_serializer = TestCaseSerializer(test_case)

        return Response(test_case_serializer.data)

    def put(self, request, unique_code, number, format=None):
        test_case = get_object_or_404(TestCase, question__unique_code=unique_code, number=number)
        if request.user != test_case.question.author:
            return JsonResponse({"error":"You are not allowed to edit this test case details"})

        serializer = TestCaseSerializer(test_case, request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)