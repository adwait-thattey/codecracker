from django.contrib.auth.models import User
from django.test import TestCase
from registration.models import *


class InstituteModelTest(TestCase):

    def test_string_representation(self):
        name = Institute(name="sample institute")
        self.assertEqual(str(name), Institute.name)


class UserProfileModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="testuser002", email="testuser002@ts.com", password="Hello World")

    def test_string_representation(self):
        user = UserProfile(user="sample user")
        self.assertEqual(str(user), UserProfile.user)


class GoogleAuthModelTest(TestCase):

    def test_string_representation(self):
        user = GoogleAuth(user="sample user")
        self.assertEqual(str(user), GoogleAuth.user)


class EmailConfirmationModelTest(TestCase):

    def test_string_representation(self):
        user = EmailConfirmation(user="sample user")
        self.assertEqual(str(user), EmailConfirmation.user)


class NotificationModelTest(TestCase):

    def test_string_representation(self):
        user = Notification(user="sample user")
        self.assertEqual(str(user), Notification.user)
