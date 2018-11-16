
from registration.forms import RegisterForm
from registration.models import UserProfile
from django.contrib.auth.models import User
from django.test import TestCase



class TestRegisterForm(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="testuser002", email="testuser002@ts.com", password="Hello World")

    def test_all_details_submitted(self):
        form_instance = RegisterForm(data={
            "user": "Sample User",
            "phone_number": 9999999999,
            "institute": "Sample institute",
            "designation":"STU",
        })

        self.assertEqual(form_instance.is_valid(), True)

        register = form_instance.save(commit=False)

        register.save()

       # model_instance = UserProfile.objects.get(**********)
        model_instance = UserProfile.objects.get(user = "Sample User")

        self.assertEqual(model_instance.user, "Sample User")
        self.assertEqual(model_instance.phone_number, 9999999999)
        self.assertEqual(model_instance.institute, "Sample institute")
        self.assertEqual(model_instance.designation, "STU")

    def test_missing_user(self):
        form_instance = RegisterForm(data={
            "phone_number": 9999999999,
            "institute": "Sample institute",
            "designation": "STU",
        })

        self.assertEqual(form_instance.is_valid(), False)
        self.assertNotEqual(form_instance.errors.get("user"), None)

    def test_missing_phone_number(self):
        form_instance = RegisterForm(data={
            "user": "Sample User",
            "institute": "Sample institute",
            "designation": "STU",
        })

        self.assertEqual(form_instance.is_valid(), False)
        self.assertNotEqual(form_instance.errors.get("phone_number"), None)

    def test_missing_institute(self):
        form_instance = RegisterForm(data={
            "user": "Sample User",
            "phone_number": 9999999999,
            "designation": "STU",
        })

        self.assertEqual(form_instance.is_valid(), False)
        self.assertNotEqual(form_instance.errors.get("institute"), None)

    def test_missing_designation(self):
        form_instance = RegisterForm(data={
            "user": "Sample User",
            "phone_number": 9999999999,
            "institute": "Sample institute",
        })

        self.assertEqual(form_instance.is_valid(), False)
        self.assertNotEqual(form_instance.errors.get("designation"), None)

