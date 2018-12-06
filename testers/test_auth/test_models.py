from django.contrib.auth.models import User
from django.test import TestCase
from registration.models import *


class InstituteModelTest(TestCase):

    #def test_string_representation(self):

        def setUp(self):
            self.name = Institute.objects.create(name= "sample institute")
        # name = Institute(name="sample institute")
        def Create_Model(self):
            name=self.name
            return Institute.objects.create(name=name)

        def test_model_creation(self):
            x = self.Create_Model()
            self.assertTrue(isinstance(x, Institute))
            self.assertEqual(x.__str__(), x.name)

        # self.assertEqual("sample institute", Institute.name)


class UserProfileModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="testuser002", email="testuser002@ts.com", password="Hello World")
        self.name = Institute.objects.create(name="sample institution")

    def Create_Institute_Model(self):
        name = self.name
        return Institute.objects.create(name=name)

    # def test_string_representation(self):
    #     user = UserProfile(user=User)
    #     self.assertEqual(__str__(user), UserProfile.user)
    def Create_Model(self, phone_number=99999999999,  designation="STU"):
        user = self.user
        institute= self.Create_Institute_Model()
        return UserProfile.objects.create(user=user,
                                          phone_number=phone_number,
                                          institute=institute,
                                          designation=designation)

    def test_model_creation(self):
        x = self.Create_Model()
        self.assertTrue(isinstance(x, UserProfile))
        self.assertEqual(x.__str__(), x.user)


class GoogleAuthModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="testuser002", email="testuser002@ts.com", password="Hello World")

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
        x = self.create_Model()
        self.assertTrue(isinstance(x, GoogleAuth))
        self.assertEqual(x.__str__(), x.user)


class EmailConfirmationModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="testuser002", email="testuser002@ts.com", password="Hello World")

    def create_Model(self, email_confirmed="True"):
        user = EmailConfirmation(user=self.user)
        return EmailConfirmation.objects.create(user=user,
                                                email_confirmed=email_confirmed)

    # def test_string_representation(self):
    #     user = EmailConfirmation(user=User)
    #     self.assertEqual(str(user), EmailConfirmation.user)

    def test_model_creation(self):
        x = self.create_Model()
        self.assertTrue(isinstance(x, UserProfile))
        self.assertEqual(x.__str__(), x.user)


class NotificationModelTest(TestCase):

    # def test_string_representation(self):
    #     user = Notifications(user=User)
    #     self.assertEqual(str(user), Notifications.user)
    def create_Model(self, content="sample content", icon="sample icon", link="https://www.google.com",
                     time_stamp="2018-09-25"):
        user = Notification(user=User)
        return Notification.objects.create(user=user,
                                            content=content,
                                            icon=icon,
                                            link=link,
                                            time_stamp=time_stamp)

    def test_model_creation(self):
        x = self.create_Model()
        self.assertTrue(isinstance(x, UserProfile))
        self.assertEqual(x.__str__(), x.user)


class Phone_number_validatorTest(TestCase):

    # def test_chars_in_number(self):
    #     dummy_number = "9999999999abc"
    #     phone_number_validator(dummy_number)
    #     with self.assertRaises(ValidationError) as cm:
    #         # self.assertEqual(cm ,"Phone Number can contain only numbers ")
    #         pass
    # def test_invalid_length(self):
    #     dummy_number = 999999999999
    #     phone_number_validator(dummy_number)
    #     with self.assertRaises(ValidationError) as cm:
    #         # self.assertEqual(cm, "Length of phone number must be either 10 or 11 ")
    #         phone_number_validator()
    #     #self.assertTrue("Length of phone number must be either 10 or 11" in cm.exception)
    #         pass

    def test_phone_number_has_more_digits(self):
        dummy_number = 999999999999
        self.assertRaises(ValidationError, phone_number_validator,dummy_number)


    def test_phone_number_has_less_digits(self):
        dummy_number = 9999
        self.assertRaises(ValidationError, phone_number_validator,dummy_number)


    def test_phone_number_has_characters(self):
        dummy_number = "9999999abc"
        self.assertRaises(ValidationError, phone_number_validator, dummy_number)
