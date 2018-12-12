from django.http import Http404
from django.shortcuts import get_object_or_404
from contests.models import Contest ,ContestQuestion
from .serializers import ContestSerializer, ContestQuestionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from contests.permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import User


class Create_Contest(APIView):
    """ def perform_create(self, serializer):
            serializer.save(owner=self.request.user)
       """

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)

    def post(self, request):
            serializer = ContestSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class Edit_Contest(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)
    def get_contest(self, unique_code):
        try:
            return Contest.objects.get(unique_code=unique_code)
        except Contest.DoesNotExist:
            raise Http404

    def get(self, request, unique_code, format=None):
        contest = self.get_contest(unique_code)
        serializer = ContestSerializer(contest)
        return Response(serializer.data)

    def put(self, request, unique_code, format=None):
        contest = self.get_contest(unique_code)
        serializer = ContestSerializer(contest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, unique_code, format=None):
        contest = self.get_contest(unique_code)
        contest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class contest_question_create(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    def get_contest(self, unique_code):
        try:
            return Contest.objects.get(unique_code=unique_code)
        except Contest.DoesNotExist:
            raise Http404

    def post(self, request, unique_code):
        contest = self.get_contest(unique_code)
        print(request.data)
        serializer = ContestQuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class contest_question_edit(APIView):

    def get_contest(self, unique_code):
        try:
            return Contest.objects.get(unique_code=unique_code)
        except Contest.DoesNotExist:
            raise Http404

    def get_question(self,unique_code,number):
        try:
            return ContestQuestion.objects.get(unique_code=unique_code,question_unique_code=unique_code)
        except ContestQuestion.DoesNotExist:
            raise Http404

    def get(self, request, unique_code, number, format=None):
        question = get_object_or_404(ContestQuestion, question__unique_code=unique_code, number=number)
        contest_question_serializer = ContestQuestionSerializer(question)

        return Response(contest_question_serializer.data)


    def put(self, request, unique_code,number, format=None):
        question = self.get_question(unique_code,number)
        serializer = ContestQuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, unique_code,number, format=None):
        question = self.get_question(unique_code,number)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





