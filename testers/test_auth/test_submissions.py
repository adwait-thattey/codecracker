from registration.forms import RegisterForm
from registration.models import UserProfile, Institute
from django.contrib.auth.models import User
from django.test import TestCase, Client


class TestRegisterSubmission(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="testuser002", email="testuser002@ts.com", password="Hello World")

    def test_submission(self):
        self.client = Client()
        response = self.client.post('registration/register',
                                    {"user": "Sample User",
                                     "phone_number": 9999999999,
                                     "institute": "Sample institute",
                                     "designation": "STU", })
        self.assertEqual(response.status_code, 200)


class TestLoginSubmission(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="testuser002", email="testuser002@ts.com", password="Hello World")

    def test_submission(self):
        self.client = Client()
        response = self.client.post('registration/login',
                                    {"username": "testuser002",
                                     "password": "Hello World"})
        self.assertEqual(response.status_code, 200)



#TODO failing
class TestEditProfileSubmission(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="testuser002", email="testuser002@ts.com", password="Hello World")
        self.name = Institute.objects.create(name="sample institution")

    def test_submission(self):
        self.client = Client()
        response = self.client.post('registration/profile',
                                    {"phone_number": 99999999,
                                    "institute": self.name.id,
                                    "picture":"/profiles/default.png",
                                    "about": "sample about", })

        self.assertEqual(response.status_code, 200)
