from registration import views
from django.test import Client, TestCase
from django.contrib.auth.models import User

from registration.views import logout_view


class LogoutViewTest(TestCase):

    def setUp(self):
        self.createduser = User.objects.create_user(username="testnormaluser", email="testnormaluser@ts.com",
                                                    password="Test Hello World")
        self.client = None
        self.request_url = '/registration/logout'
        # Create clients on the fly in the tests as login/logout is required

    def test_logout_view(self):
        self.client= Client()
        self.client.force_login(self.createduser)
      #  response = logout_view(request = self.client.logout)
        response = self.client.logout()

        self.assertRedirects(response, expected_url="landing")
