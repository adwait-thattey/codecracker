from questions.forms import PostQuestionForm, SubmissionForm, TestCaseCreateForm
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
            "unique_code": "samques001",
            "constraints": "Sample constraints",
            "input_format": "sample inp format",
            "output_format": "sample_output_format",
            "sample_input": "Sample Input",
            "sample_output": "Sample Output"
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
        self.assertEqual(model_instance.constraints, "Sample constraints")
        self.assertEqual(model_instance.input_format, "sample inp format")
        self.assertEqual(model_instance.output_format, "sample_output_format")
        self.assertEqual(model_instance.sample_input, "Sample Input")
        self.assertEqual(model_instance.sample_output, "Sample Output")

    def test_missing_title(self):
        form_instance = PostQuestionForm(data={
            "short_description": "Sample Short Description",
            "description": "Sample Description",
            "time_limit": 2,
            "unique_code": "samques001",
            "constraints": "Sample constraints",
            "input_format": "sample inp format",
            "output_format": "sample_output_format",
            "sample_input": "Sample Input",
            "sample_output": "Sample Output"
        })

        self.assertEqual(form_instance.is_valid(), False)
        self.assertNotEqual(form_instance.errors.get("title"), None)

    def test_missing_short_description(self):
        form_instance = PostQuestionForm(data={
            "title": "Sample Title",
            "description": "Sample Description",
            "time_limit": 2,
            "unique_code": "samques001",
            "constraints": "Sample constraints",
            "input_format": "sample inp format",
            "output_format": "sample_output_format",
            "sample_input": "Sample Input",
            "sample_output": "Sample Output"
        })

        self.assertEqual(form_instance.is_valid(), False)
        self.assertNotEqual(form_instance.errors.get("short_description"), None)

    def test_missing_description(self):
        form_instance = PostQuestionForm(data={
            "title": "Sample Title",
            "short_description": "Sample Short Description",
            "time_limit": 2,
            "unique_code": "samques001",
            "constraints": "Sample constraints",
            "input_format": "sample inp format",
            "output_format": "sample_output_format",
            "sample_input": "Sample Input",
            "sample_output": "Sample Output"
        })

        self.assertEqual(form_instance.is_valid(), False)
        self.assertNotEqual(form_instance.errors.get("description"), None)

    def test_missing_time_limit(self):
        form_instance = PostQuestionForm(data={
            "title": "Sample Title",
            "short_description": "Sample Short Description",
            "description": "Sample Description",
            "unique_code": "samques001",
            "constraints": "Sample constraints",
            "input_format": "sample inp format",
            "output_format": "sample_output_format",
            "sample_input": "Sample Input",
            "sample_output": "Sample Output"
        })

        self.assertEqual(form_instance.is_valid(), False)
        self.assertNotEqual(form_instance.errors.get("time_limit"), None)

    def test_missing_unique_code(self):
        form_instance = PostQuestionForm(data={
            "title": "Sample Title",
            "short_description": "Sample Short Description",
            "description": "Sample Description",
            "time_limit": 2,
            "constraints": "Sample constraints",
            "input_format": "sample inp format",
            "output_format": "sample_output_format",
            "sample_input": "Sample Input",
            "sample_output": "Sample Output"
        })

        self.assertEqual(form_instance.is_valid(), False)
        self.assertNotEqual(form_instance.errors.get("unique_code"), None)

    def test_missing_consraints(self):
        form_instance = PostQuestionForm(data={
            "title": "Sample Title",
            "short_description": "Sample Short Description",
            "description": "Sample Description",
            "time_limit": 2,
            "unique_code": "samques001",
            "input_format": "sample inp format",
            "output_format": "sample_output_format",
            "sample_input": "Sample Input",
            "sample_output": "Sample Output"
        })

        self.assertEqual(form_instance.is_valid(), False)

    def test_missing_input_format(self):
        form_instance = PostQuestionForm(data={
            "title": "Sample Title",
            "short_description": "Sample Short Description",
            "description": "Sample Description",
            "time_limit": 2,
            "unique_code": "samques001",
            "constraints": "Sample constraints",
            "output_format": "sample_output_format",
            "sample_input": "Sample Input",
            "sample_output": "Sample Output"
        })

        self.assertEqual(form_instance.is_valid(), False)

    def test_missing_output_format(self):
        form_instance = PostQuestionForm(data={
            "title": "Sample Title",
            "short_description": "Sample Short Description",
            "description": "Sample Description",
            "time_limit": 2,
            "unique_code": "samques001",
            "constraints": "Sample constraints",
            "input_format": "sample inp format",
            "sample_input": "Sample Input",
            "sample_output": "Sample Output"
        })

        self.assertEqual(form_instance.is_valid(), False)

    def test_missing_sample_input(self):
        form_instance = PostQuestionForm(data={
            "title": "Sample Title",
            "short_description": "Sample Short Description",
            "description": "Sample Description",
            "time_limit": 2,
            "unique_code": "samques001",
            "constraints": "Sample constraints",
            "input_format": "sample inp format",
            "output_format": "sample_output_format",
            "sample_output": "Sample Output"
        })

        self.assertEqual(form_instance.is_valid(), False)

    def test_missing_sample_output(self):
        form_instance = PostQuestionForm(data={
            "title": "Sample Title",
            "short_description": "Sample Short Description",
            "description": "Sample Description",
            "time_limit": 2,
            "unique_code": "samques001",
            "constraints": "Sample constraints",
            "input_format": "sample inp format",
            "output_format": "sample_output_format",
            "sample_input": "Sample Input"
        })

        self.assertEqual(form_instance.is_valid(), False)


class TestSubmissionForm(TestCase):
    pass


class TestTestCaseForm(TestCase):
    pass
