from questions.forms import PostQuestionForm, SubmissionForm, TestCaseCreateForm
from questions.models import Question, Submission, TestCase
from django.contrib.auth.models import User
from django.test import TestCase
class SubmissionTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="testuser002", email="testuser002@ts.com", password="Hello World")
    def test_all_details_submitted(self):
        form_instance = SubmissionForm(data={
            "language"="some",
            "code"="sample code"
        })

        self.assertEqual(form_instance.is_valid(), True)

        question = form_instance.save(commit=False)
        question.author = self.user
        question.save()
    