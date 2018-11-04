from django.test import Client, TestCase


# TODO Set tests for logged in users, having different configurations like with and without more_user_data
# Check this out for above : https://docs.djangoproject.com/en/2.1/topics/testing/advanced/#example

class BlankUrlTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_anonymous_ping(self):
        response = self.client.get('')

        self.assertRedirects(response, expected_url='/index')


class IndexTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_anonymous_ping(self):
        response = self.client.get('/index')

        self.assertEqual(response.status_code, 404)


class HomeTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_anonymous_ping(self):
        response = self.client.get('/home')

        self.assertEqual(response.status_code, 200)
