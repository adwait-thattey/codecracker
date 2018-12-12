
from django.http import request

from registration.forms import RegisterForm, ProfileEditForm, UserProfileForm
from registration.models import UserProfile, Institute

from django.contrib.auth.models import User
from django.test import TestCase



class TestUserProfileForm(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="testuser002", email="testuser002@ts.com", password="Hello World")
        self.name = Institute.objects.create(name="sample institution")

    def test_all_details_submitted(self):
        form_instance = UserProfileForm(instance=self.user.userprofile, data={
            "user": self.user.id,
            "phone_number": "9999999999",
            "institute": self.name.id,
            "designation":"STU",
        })

        if not form_instance.is_valid():
            print(form_instance.errors)
        self.assertEqual(form_instance.is_valid(), True)

        register = form_instance.save(commit=False)

        register.save()

        model_instance = UserProfile.objects.get(user = "Sample User")

        self.assertEqual(model_instance.user, "Sample User")
        self.assertEqual(model_instance.phone_number, 9999999999)
        self.assertEqual(model_instance.institute, self.name)
        self.assertEqual(model_instance.designation, "STU")

    def test_missing_user(self):
        form_instance = UserProfileForm(data={
            "phone_number": 9999999999,
            "institute": "Sample institute",
            "designation": "STU",
        })

        self.assertEqual(form_instance.is_valid(), False)
        self.assertNotEqual(form_instance.errors.get("user"), None)

    def test_missing_phone_number(self):
        form_instance = UserProfileForm(data={
            "user": "Sample User",
            "institute": "Sample institute",
            "designation": "STU",
        })

        self.assertEqual(form_instance.is_valid(), False)
        self.assertEqual(form_instance.errors.get("phone_number"), None)

    def test_missing_institute(self):
        form_instance = UserProfileForm(data={
            "user": "Sample User",
            "phone_number": 9999999999,
            "designation": "STU",
        })

        self.assertEqual(form_instance.is_valid(), False)
        self.assertEqual(form_instance.errors.get("institute"), None)

    def test_missing_designation(self):
        form_instance = UserProfileForm(data={
            "user": "Sample User",
            "phone_number": 9999999999,
            "institute": "Sample institute",
        })

        self.assertEqual(form_instance.is_valid(), False)
        self.assertNotEqual(form_instance.errors.get("designation"), None)

class ProfileEditFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(first_name="test", last_name="user", username="testuser",
                                        email="testuser002@ts.com")

        self.name = Institute.objects.create(name="sample institution")

    def test_all_details_submitted(self):
        form_instance = ProfileEditForm(data={
            "phone_number": 99999999,
            "institute": self.name.id,
            "picture":"/profiles/default.png",
            "about": "sample about",
        })

        self.assertEqual(form_instance.is_valid(), True)

        ProfileEdit = form_instance.save(commit=False)

        ProfileEdit.save()

    def test_missing_phone_number(self):
        form_instance = ProfileEditForm(data={
            "institute": self.name.id,
            "picture":"/profiles/default.png",
            "about": "sample about",
        })

        #form is valid because phone number is not a required field
        self.assertEqual(form_instance.is_valid(), True)
        self.assertEqual(form_instance.errors.get("phone_number"), None)

    def test_missing_institute(self):
        form_instance = ProfileEditForm(data={
            "phone_number": 99999999,
            "picture": "/profiles/default.png",
            "about": "sample about",
        })

        # form is not valid because institute is  a required field
        self.assertEqual(form_instance.is_valid(), False)
        self.assertEqual(form_instance.errors.get("institute"), None)

    def test_missing_picture(self):
        form_instance = ProfileEditForm(data={
            "phone_number": 99999999,
            "institute": self.name.id,
            "about": "sample about",
        })

        # form is not valid because institute is  a required field
        self.assertEqual(form_instance.is_valid(), False)
        self.assertEqual(form_instance.errors.get("picture"), None)

    def test_missing_about(self):
        form_instance = ProfileEditForm(data={
            "phone_number": 99999999,
            "institute": self.name.id,
            "picture": "/profiles/default.png",
        })

        # form is not valid because institute is  a required field
        self.assertEqual(form_instance.is_valid(), False)
        self.assertEqual(form_instance.errors.get("picture"), None)

class TestRegisterForm(TestCase):

    def setUp(self):
            self.user = User.objects.create(first_name="test",last_name = "user", username="testuser",email="testuser002@ts.com")

    def test_all_details_submitted(self):
        form_instance = RegisterForm(data={
            "first_name": "test",
            "last_name": "user",
            "username": "testuser",
            "email" : "testuser002@ts.com",
            "password" : "qwerty123",
            "confirm_password": "qwerty123",
        })

        self.assertEqual(form_instance.is_valid(), True)

        register = form_instance.save(commit=False)

        register.save()

    def test_missing_first_name(self):
        form_instance = RegisterForm(data={
            "last_name": "user",
            "username": "testuser",
            "email": "testuser002@ts.com",
            "password": "qwerty123",
            "confirm_password": "qwerty123",
        })

        self.assertEqual(form_instance.is_valid(), False)
        self.assertEqual(form_instance.errors.get("first_name"), None)


    def test_missing_last_name(self):
        form_instance = RegisterForm(data={
            "first_name": "test",
            "username": "testuser",
            "email": "testuser002@ts.com",
            "password": "qwerty123",
            "confirm_password": "qwerty123",
        })

        self.assertEqual(form_instance.is_valid(), False)
        self.assertEqual(form_instance.errors.get("last_name"), None)


    def test_missing_username(self):
        form_instance = RegisterForm(data={
            "first_name": "test",
            "last_name": "user",
            "email": "testuser002@ts.com",
            "password": "qwerty123",
            "confirm_password": "qwerty123",
        })

        self.assertEqual(form_instance.is_valid(), False)
        self.assertNotEqual(form_instance.errors.get("username"), None)

    def test_missing_email(self):
        form_instance = RegisterForm(data={
            "first_name": "test",
            "last_name": "user",
            "username": "testuser",
            "password": "qwerty123",
            "confirm_password": "qwerty123",
        })

        self.assertEqual(form_instance.is_valid(), False)
        self.assertEqual(form_instance.errors.get("email"), None)


    def test_missing_password(self):
        form_instance = RegisterForm(data={
            "first_name": "test",
            "last_name": "user",
            "username": "testuser",
            "email": "testuser002@ts.com",
            "confirm_password": "qwerty123",
        })

        self.assertEqual(form_instance.is_valid(), False)
        self.assertNotEqual(form_instance.errors.get("password"), None)

    def test_missing_confirm_password(self):
        form_instance = RegisterForm(data={
            "first_name": "test",
            "last_name": "user",
            "username": "testuser",
            "email": "testuser002@ts.com",
            "password": "qwerty123",
        })

        self.assertEqual(form_instance.is_valid(), False)
        self.assertNotEqual(form_instance.errors.get("confirm_password"), None)

    def test_duplicate_username(self):
        form_instance = RegisterForm(data={
            "first_name": "test",
            "last_name": "user",
            "username": "testuser",
            "email" : "testuser02@ts.com",
            "password": "qwerty123",
            "confirm_password": "qwerty123",
        })

        self.assertEqual(form_instance.is_valid(),False)

    def test_duplicate_email(self):
        form_instance = RegisterForm(data={
            "first_name": "test",
            "last_name": "user",
            "username": "testuser1",
            "email" : "testuser002@ts.com",
            "password": "qwerty123",
            "confirm_password": "qwerty123",
        })

        self.assertEqual(form_instance.is_valid(),False)

    def test_passwords_donot_match(self):
        form_instance = RegisterForm(data={
            "first_name": "test",
            "last_name": "user",
            "username": "testuser1",
            "email": "testuser002@ts.com",
            "password": "qwerty123",
            "confirm_password": "qwerty12345",
        })

        self.assertEqual(form_instance.is_valid(), False)

