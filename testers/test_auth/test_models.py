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

    # def test_string_representation(self):
    #     user = UserProfile(user=User)
    #     self.assertEqual(__str__(user), UserProfile.user)

    def Create_Model(self, phone_number=99999999999, institute="sample institute", designation="STU"):
        user = self.user
        return UserProfile.objects.create(user=user,
                                          phone_number=phone_number,
                                          institute=institute,
                                          designation=designation)

    def test_model_creation(self):
        x = self.Create_Model()
        self.assertTrue(isinstance(x, UserProfile))
        self.assertEqual(x.__str__(), x.user)


class GoogleAuthModelTest(TestCase):

    def create_Model(self, google_id="sample id", salt="sample salt"):
        user = GoogleAuth(user=User)
        return GoogleAuth.objects.create(user=user,
                                         google_id=google_id,
                                         salt=salt,
                                         )



# def test_string_representation(self):
#     user = GoogleAuth(user=User)
#     self.assertEqual(str(user), GoogleAuth.user)

def test_model_creation(self):
    x = self.Create_Model()
    self.assertTrue(isinstance(x, UserProfile))
    self.assertEqual(x.__str__(), x.user)


class EmailConfirmationModelTest(TestCase):

    def create_Model(self, email_confirmed="True"):
        user = EmailConfirmation(user=User)
        return EmailConfirmation.objects.create(user=user,
                                                email_confirmed=email_confirmed)

    # def test_string_representation(self):
    #     user = EmailConfirmation(user=User)
    #     self.assertEqual(str(user), EmailConfirmation.user)

    def test_model_creation(self):
        x = self.Create_Model()
        self.assertTrue(isinstance(x, UserProfile))
        self.assertEqual(x.__str__(), x.user)


class NotificationsModelTest(TestCase):

    # def test_string_representation(self):
    #     user = Notifications(user=User)
    #     self.assertEqual(str(user), Notifications.user)
    def create_Model(self, content="sample content", icon="sample icon", link="https://www.google.com",
                     time_stamp="2018-09-25"):
        user = Notifications(user=User)
        return Notifications.objects.create(user=user,
                                            content=content,
                                            icon=icon,
                                            link=link,
                                            time_stamp=time_stamp)

    def test_model_creation(self):
        x = self.Create_Model()
        self.assertTrue(isinstance(x, UserProfile))
        self.assertEqual(x.__str__(), x.user)
