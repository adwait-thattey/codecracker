from questions.forms import PostQuestionForm, SubmissionForm, TestCaseForm
from questions.models import Question, Submission, TestCase
from django.contrib.auth.models import User
from django.test import TestCase


class TestPostQuestionForm(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="testuser002", email="testuser002@ts.com", password="Hello World")

    def test_all_details_submitted(self):
        form_instance = PostQuestionForm(data={
            "title": "Sample Title",
            "short_description": "Sample Short Description",
            "description": "Sample Description",
            "time_limit": 2,
            "unique_code": "samques001"
        })

        self.assertEqual(form_instance.is_valid(), True)

        question = form_instance.save(commit=False)
        question.author = self.user
        question.save()

        model_instance = Question.objects.get(unique_code="samques001")

        self.assertEqual(model_instance.title, "Sample Title")
        self.assertEqual(model_instance.short_description, "Sample Short Description")
        self.assertEqual(model_instance.description, "Sample Description")
        self.assertEqual(model_instance.time_limit, 2.0)

    def test_missing_title(self):
        form_instance = PostQuestionForm(data={
            "short_description": "Sample Short Description",
            "description": "Sample Description",
            "time_limit": 2,
            "unique_code": "samques001"
        })

        self.assertEqual(form_instance.is_valid(), False)
        self.assertNotEqual(form_instance.errors.get("title"), None)

    def test_missing_short_description(self):
        form_instance = PostQuestionForm(data={
            "title": "Sample Title",
            "description": "Sample Description",
            "time_limit": 2,
            "unique_code": "samques001"
        })

        self.assertEqual(form_instance.is_valid(), False)
        self.assertNotEqual(form_instance.errors.get("short_description"), None)

    def test_missing_description(self):
        form_instance = PostQuestionForm(data={
            "title": "Sample Title",
            "short_description": "Sample Short Description",
            "time_limit": 2,
            "unique_code": "samques001"
        })

        self.assertEqual(form_instance.is_valid(), False)
        self.assertNotEqual(form_instance.errors.get("description"), None)

    def test_missing_time_limit(self):
        form_instance = PostQuestionForm(data={
            "title": "Sample Title",
            "short_description": "Sample Short Description",
            "description": "Sample Description",
            "unique_code": "samques001"
        })

        self.assertEqual(form_instance.is_valid(), False)
        self.assertNotEqual(form_instance.errors.get("time_limit"), None)

    def test_missing_unique_code(self):
        form_instance = PostQuestionForm(data={
            "title": "Sample Title",
            "short_description": "Sample Short Description",
            "description": "Sample Description",
            "time_limit": 2,
        })

        self.assertEqual(form_instance.is_valid(), False)
        self.assertNotEqual(form_instance.errors.get("unique_code"), None)


class TestSubmissionForm(TestCase):
    pass


class TestTestCaseForm(TestCase):
    pass
