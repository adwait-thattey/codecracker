import os

from django.test import Client, TestCase
from django.contrib.auth.models import User
from questions.models import Question, Submission
from questions.models import TestCase as QTC
from django.conf import settings
from django.core.files import File


class SubmitSolutionTest(TestCase):

    def setUp(self):
        self.createduser = User.objects.create_user(username="testnormaluser", email="testnormaluser@ts.com",
                                                    password="Test Hello World")
        self.createduser.emailconfirmation.email_confirmed = True
        self.createduser.emailconfirmation.save()

        self.question = Question.objects.create(author=self.createduser, title="Sample Question",
                                                short_description="Sample Short Desc", description="Sample Descrption",
                                                unique_code="sq")
        
        self.client = None
        self.request_url = '/questions/' + self.question.unique_code + "/submit"

    def test_anonymous_ping(self):
        self.client = Client()
        correct_code_path = os.path.join(settings.MEDIA_ROOT, 'code_tests', 'correct_code.py')
        f = open(correct_code_path)
        response = self.client.post(self.request_url, {'language': 'PY3', 'code': f})
        self.assertRedirects(response, expected_url="/registration/login?next=" + self.request_url)
        f.close()

    def test_all_submitted(self):
        self.client = Client()
        self.client.force_login(self.createduser)
        correct_code_path = os.path.join(settings.MEDIA_ROOT, 'code_tests', 'correct_code.py')
        f = open(correct_code_path)
        response = self.client.post(self.request_url, {'language': 'PY3', 'code': f})
        self.assertRedirects(response, expected_url="/questions/sq/testnormaluser/submission/1/result")
        f.close()

        self.assertTrue(Submission.objects.filter(question=self.question, user=self.createduser).exists())

    def test_missing_code_file(self):
        self.client = Client()
        self.client.force_login(self.createduser)
        correct_code_path = os.path.join(settings.MEDIA_ROOT, 'code_tests', 'correct_code.py')
        response = self.client.post(self.request_url, {'language': 'PY3'})
        self.assertEqual(response.status_code, 200) #Back to same page with errors



# def create_test_case(self, unique_code):
#     	input_file = os.path.join(settings.MEDIA_ROOT, 'code_tests', 'sample_input.txt')
#     	output_file = os.path.join(settings.MEDIA_ROOT, 'code_tests', 'sample_output.txt')
#     	client = Client()
#     	client.force_login(self.createduser)
#     	i = open(input_file, 'r')
#     	o = open(output_file, 'r')
#     	client.post('/questions/' + unique_code + '/testcases/new',{'input_file':i, 'output_file':o, 'points':10})
#     	i.close()
#     	o.close()
#     
# self.create_test_case(self.question.unique_code)
class TestCaseNew(TestCase):
    def setUp(self):
        self.createduser = User.objects.create_user(username="testnormaluser", email="testnormaluser@ts.com",
                                                    password="Test Hello World")
        self.createduser.emailconfirmation.email_confirmed = True
        self.createduser.emailconfirmation.save()
        self.question = Question.objects.create(author=self.createduser, title="Sample Question",
                                                short_description="Sample Short Desc", description="Sample Descrption",
                                                unique_code="sq")
        
        self.client = None
        self.request_url = '/questions/' + self.question.unique_code + '/testcases/new'

    def test_anonymous_ping(self):
        input_file = os.path.join(settings.MEDIA_ROOT, 'code_tests', 'sample_input.txt')
        output_file = os.path.join(settings.MEDIA_ROOT, 'code_tests', 'sample_output.txt')
        client = Client()
        client.force_login(self.createduser)
        i = open(input_file, 'r')
        o = open(output_file, 'r')
        client.post(self.request_url,{'input_file':i, 'output_file':o, 'points':10})
        i.close()
        o.close()
    def test_all_submitted(self):
        self.client = Client()
        self.client.force_login(self.createduser)

        input_file = os.path.join(settings.MEDIA_ROOT, 'code_tests', 'sample_input.txt')
        output_file = os.path.join(settings.MEDIA_ROOT, 'code_tests', 'sample_output.txt')
        #correct_code_path = os.path.join(settings.MEDIA_ROOT, 'code_tests', 'sample_input.txt')
        i=open(input_file,'r')
        o=open(output_file,'r')
        response = self.client.post(self.request_url, {'input_file':i, 'output_file':o, 'points':10})
        self.assertRedirects(response, expected_url="/questions/sq/testcases/view")
        i.close()
        o.close()

        #self.assertTrue(Submission.objects.filter(question=self.question, user=self.createduser).exists())

    def test_missing_code_file(self):
        self.client = Client()
        self.client.force_login(self.createduser)

        input_file = os.path.join(settings.MEDIA_ROOT, 'code_tests', 'sample_input.txt')
        output_file = os.path.join(settings.MEDIA_ROOT, 'code_tests', 'sample_output.txt')
        
        i=open(input_file,'r')
        o=open(output_file,'r')
        response = self.client.post(self.request_url, {'input_file':i, 'output_file':o, 'points':10})
        self.assertRedirects(response,expected_url="/questions/sq/testcases/view") 
        i.close()
        o.close()