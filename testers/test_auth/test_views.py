from registration import views
from django.test import Client, TestCase
from django.contrib.auth.models import User

from registration.models import Institute
from registration.views import logout_view


class LogoutViewTest(TestCase):

    def setUp(self):
        self.createduser = User.objects.create_user(username="testnormaluser", email="testnormaluser@ts.com",
                                                    password="Test Hello World")
        self.client = None
      #  self.request_url = '/registration/log'
        # Create clients on the fly in the tests as login/logout is required

    def test_logout_view(self):
        self.client= Client()
        self.client.force_login(self.createduser)
      #  response = logout_view(request = self.client.logout)
        response = self.client.logout()

        self.assertRedirects(response, expected_url="landing")


class SignupViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="testuser002", email="testuser002@ts.com", password="Hello World")
        self.name = Institute.objects.create(name="sample institution")

    def Create_Institute_Model(self):
        name = self.name
        return Institute.objects.create(name=name)

    def Register_form(self):
        self.client = Client()
        new_user_form = self.client.post('registration/register',
                                    {
                                        "first_name": "test",
                                        "last_name": "user",
                                        "username": "testuser",
                                        "email": "testuser002@ts.com",
                                        "password": "qwerty123",
                                        "confirm_password": "qwerty123",
                                    })

        new_user = User.objects.create_user(
            username=new_user_form.cleaned_data["username"],
            password=new_user_form.cleaned_data["password"],
            email=new_user_form.cleaned_data["email"]
        )

        new_user.first_name = new_user_form.cleaned_data["first_name"]
        new_user.last_name = new_user_form.cleaned_data["last_name"]
        new_user.save()