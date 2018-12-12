from questions.forms import PostQuestionForm, SubmissionForm, TestCaseCreateForm
from questions.models import Question, Submission, TestCase, Category
from django.contrib.auth.models import User
from django.test import TestCase
import os
from django.conf import settings
from django.core.files import File


class TestPostQuestionForm(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="testuser002", email="testuser002@ts.com", password="Hello World")
        self.cat = Category.objects.create(name="samcat1", description="Sample Category 1")
    def test_all_details_submitted(self):
        form_instance = PostQuestionForm(data={
            "title": "Sample Title",
            "category": self.cat,
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


'''class TestSubmissionForm(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser002", email="testuser002@ts.com", password="Hello World")
    def test_all_details_submitted(self):
        f = os.path.join(settings.MEDIA_ROOT, 'code_tests', 'correct_code.py')
        # F = File(open(f))
        form_instance = SubmissionForm(data={
            "language":"PY3",
            "code":F
        })

        self.assertEqual(form_instance.is_valid(), True)

        question = form_instance.save(commit=False)
        question.author = self.user
        question.save()

        model_instance = Submission.objects.get(language="Samplelangauage")

        self.assertEqual(model_instance.code, "Samplecode")

     def test_missing_langauage(self):
         form_instance = SubmissionForm(data={
             "code": "Samplecode",

         })

         self.assertEqual(form_instance.is_valid(), False)
         self.assertNotEqual(form_instance.errors.get("language"), None)

     def test_missing_code(self):
         form_instance = SubmissionForm(data={
             "language": "Samplelangauage",

         })

         self.assertEqual(form_instance.is_valid(), False)        
         self.assertNotEqual(form_instance.errors.get("code"), None)
class TestTestCaseForm(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser002", email="testuser002@ts.com", password="Hello World")
    def test_all_details_submitted(self):
        
        form_instance = TestCaseCreateForm(data={
            "input_file":"Sampleinputfile",
            "output_file":"Sampleoutputfile",
            "points":2,
        })

        self.assertEqual(form_instance.is_valid(), True)

        question = form_instance.save(commit=False)
        question.author = self.user
        question.save()

        model_instance = TestCase.objects.get(input_file="Sampleinputfile")

        self.assertEqual(model_instance.output_file, "Sampleoutputfile")
        self.assertEqual(model_instance.points, 2)

    def test_missing_input_file(self):
        form_instance = TestCaseCreateForm(data={
            "output_file": "Sampleoutputfile",
            "points":2,

        })

        self.assertEqual(form_instance.is_valid(), False)
        self.assertNotEqual(form_instance.errors.get("input_file"), None)        

    def test_missing_output_file(self):
        form_instance = TestCaseCreateForm(data={
            "input_file": "Sampleinputfile",
            "points":2,

        })
        self.assertEqual(form_instance.is_valid(), False)
        self.assertNotEqual(form_instance.errors.get("output_file"), None)
    def test_missing_points(self):
        form_instance = TestCaseCreateForm(data={
            "input_file": "Sampleinputfile",
            "output_file":"Sampleoutputfile",

        })

        self.assertEqual(form_instance.is_valid(), False)        

        self.assertNotEqual(form_instance.errors.get("points"), None)'''