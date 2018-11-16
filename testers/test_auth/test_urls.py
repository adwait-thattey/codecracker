from django.test import Client, TestCase
from django.contrib.auth.models import User


class RegisterTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_anonymous_ping(self):
        response = self.client.get('/registration/register')

        self.assertEqual(response.status_code, 200)




class RegisterUrlTest(TestCase):

    def setUp(self):
        self.createduser = User.objects.create_user(username="testnormaluser", email="testnormaluser@ts.com",
                                                    password="Test Hello World")
        self.client = None
        self.request_url = '/registration/register'
        # Create clients on the fly in the tests as login/logout is required

    def test_anonymous_ping(self):
        self.client = Client()
        response = self.client.get(self.request_url)

        self.assertEqual(response.status_code,200)

    def test_authenticated_ping(self):
        self.client = Client()
        self.client.force_login(self.createduser)
        response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)

    def test_authenticated_random_id_ping(self):
        self.client = Client()
        self.client.force_login(self.createduser)
        response = self.client.get('registarion/register/blahblah')
        self.assertEqual(response.status_code, 404)




class LoginUrlTest(TestCase):

    def setUp(self):
        self.createduser = User.objects.create_user(username="testnormaluser", email="testnormaluser@ts.com",
                                                    password="Test Hello World")
        self.client = None
        self.request_url = '/registration/login'
        # Create clients on the fly in the tests as login/logout is required

    def test_anonymous_ping(self):
        self.client = Client()
        response = self.client.get(self.request_url)

        self.assertRedirects(response, expected_url="/registration/login" )

    def test_authenticated_ping(self):
        self.client = Client()
        self.client.force_login(self.createduser)
        response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)

    def test_authenticated_random_id_ping(self):
        self.client = Client()
        self.client.force_login(self.createduser)
        response = self.client.get('registration/login/blahblah')
        self.assertEqual(response.status_code, 404)

