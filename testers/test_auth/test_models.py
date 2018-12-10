from django.contrib.auth.models import User
from django.test import TestCase
from registration.models import *


class InstituteModelTest(TestCase):

        def setUp(self):
            self.name = Institute.objects.create(name= "sample institute")

        def Create_Model(self):
            name=self.name
            return Institute.objects.create(name=name)

        def test_model_creation(self):
            x = self.Create_Model()
            self.assertTrue(isinstance(x, Institute))
            self.assertEqual(x.__str__(), x.name)


class UserProfileModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="testuser002", email="testuser002@ts.com", password="Hello World")
        self.name = Institute.objects.create(name="sample institution")

    def test_model_creation(self):
      self.assertTrue(UserProfile.objects.filter(user__username='testuser002').exists())

class GoogleAuthModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="testuser002", email="testuser002@ts.com", password="Hello World")

    def create_Model(self, google_id="sample id", salt="sample salt"):
        user = GoogleAuth(user=User)
        return GoogleAuth.objects.create(user=user,
                                         google_id=google_id,
                                         salt=salt,
                                         )

    def test_model_creation(self):
        # x = self.create_Model()
        # self.assertTrue(isinstance(x, GoogleAuth))
        # self.assertEqual(x.__str__(), x.user)
        self.assertTrue(hasattr(self.user, 'googleauth'))

class EmailConfirmationModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="testuser002", email="testuser002@ts.com", password="Hello World")

    def test_model_creation(self):
        self.assertTrue(hasattr(self.user, 'emailconfirmation'))

class NotificationModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="testuser002", email="testuser002@ts.com", password="Hello World")

    def create_Model(self, content="sample content", icon="sample icon", link="landing",
                      time_stamp="2018-09-25"):
         user = Notification(user=User)
         return Notification.objects.create(user=user,
                                             content=content,
                                             icon=icon,
                                             link=link,
                                             time_stamp=time_stamp)

    def test_model_creation(self):
        self.assertTrue(hasattr(self.user, 'notification_set'))


class Phone_number_validatorTest(TestCase):

    def test_phone_number_has_more_digits(self):
        dummy_number = 999999999999
        self.assertRaises(ValidationError, phone_number_validator,dummy_number)

    def test_phone_number_has_less_digits(self):
        dummy_number = 9999
        self.assertRaises(ValidationError, phone_number_validator,dummy_number)

    def test_phone_number_has_characters(self):
        dummy_number = "9999999abc"
        self.assertRaises(ValidationError, phone_number_validator, dummy_number)