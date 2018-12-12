from django.contrib.auth.models import User
from django.test import TestCase
from contests.models import *


class ContestModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="testuser002", email="testuser002@ts.com", password="Hello World")
        self.contest = Contest.objects.create(author=self.user, title="Sample Question",
                                              short_description="Sample Short Desc", description="Sample Descrption",
                                              unique_code="sqdffe", start_date="12/12/12", end_date="13/12/12",
                                              is_public=True, participants=self.user)

    def test_model_creation(self):
      self.assertTrue(Contest.objects.filter(unique_code='sqdffe').exists())
      self.assertEqual(self.contest.__str__(),self.contest.unique_code)


class ContestQuestionModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="testuser002", email="testuser002@ts.com", password="Hello World")

        self.contest = Contest.objects.create(author=self.user, title="Sample Question",
                                              short_description="Sample Short Desc", description="Sample Descrption",
                                              unique_code="sqdffe", start_date="12/12/12", end_date="13/12/12",
                                              is_public=True, participants=self.user)

        self.question = Question.objects.create(author=self.user, title="Sample Question",
                                                short_description="Sample Short Desc", description="Sample Descrption",
                                                unique_code="sq")

    def test_model_creation(self):
        points = self.contest.objects.values(points=50)
