
from django.test import Client, TestCase
from django.contrib.auth.models import User
from contests.models import *
from questions.models import Question

class ContestEditUrlTest(TestCase):

    def setUp(self):
        self.createduser = User.objects.create_user(username="testnormaluser", email="testnormaluser@ts.com",
                                                    password="Test Hello World")
        self.contest = Contest.objects.create(author=self.createduser, title="Sample Question",
                                                short_description="Sample Short Desc", description="Sample Descrption",
                                                unique_code="sqdffe",start_date = "12/12/12",end_date="13/12/12",is_public=True,participants = self.createduser)
        self.client = None
        self.request_url = '/contests/' + self.contest.unique_code+ "/edit"
        # Create clients on the fly in the tests as login/logout is required

    def test_anonymous_ping(self):
        self.client = Client()
        response = self.client.get(self.request_url)

        #self.assertEqual(response.status_code,200)
        self.assertRedirects(response, expected_url="/registration/login?next=" + self.request_url)

    def test_authenticated_ping(self):
        self.client = Client()
        self.client.force_login(self.createduser)
        response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)

    def test_authenticated_random_id_ping(self):
        self.client = Client()
        self.client.force_login(self.createduser)
        response = self.client.get('/contests/' + self.contest.unique_code+ "/edit/blahblah")
        self.assertEqual(response.status_code, 404)

class ContestCreateUrlTest(TestCase):

    def setUp(self):
        self.createduser = User.objects.create_user(username="testnormaluser", email="testnormaluser@ts.com",
                                                    password="Test Hello World")
        self.contest = Contest.objects.create(author=self.createduser, title="Sample Question",
                                              short_description="Sample Short Desc", description="Sample Descrption",
                                              unique_code="sqdffe", start_date="12/12/12", end_date="13/12/12",
                                              is_public=True, participants=self.createduser)
        self.client = None
        self.request_url = '/contests/' + "create"

    def test_anonymous_ping(self):
        self.client = Client()
        response = self.client.get(self.request_url)

        #self.assertEqual(response.status_code,200)
        self.assertRedirects(response, expected_url="/registration/login?next=" + self.request_url)

    def test_authenticated_ping(self):
        self.client = Client()
        self.client.force_login(self.createduser)
        response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)

    def test_authenticated_random_id_ping(self):
        self.client = Client()
        self.client.force_login(self.createduser)
        response = self.client.get('/contests/' + "create/blahblah")
        self.assertEqual(response.status_code, 404)


class ContestQuestionCreateUrlTest(TestCase):

    def setUp(self):
        self.createduser = User.objects.create_user(username="testnormaluser", email="testnormaluser@ts.com",
                                                    password="Test Hello World")
        self.contest = Contest.objects.create(author=self.createduser, title="Sample Question",
                                                short_description="Sample Short Desc", description="Sample Descrption",
                                                unique_code="sqdffe",start_date = "12/12/12",end_date="13/12/12",is_public=True,participants = self.createduser)

        self.client = None
        self.request_url = '/contests/' + self.contest.unique_code+ "questions/create"
        # Create clients on the fly in the tests as login/logout is required

    def test_anonymous_ping(self):
        self.client = Client()
        response = self.client.get(self.request_url)

        #self.assertEqual(response.status_code,200)
        self.assertRedirects(response, expected_url="/registration/login?next=" + self.request_url)

    def test_authenticated_ping(self):
        self.client = Client()
        self.client.force_login(self.createduser)
        response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)

    def test_authenticated_random_id_ping(self):
        self.client = Client()
        self.client.force_login(self.createduser)
        response = self.client.get('/contests/' + self.contest.unique_code+ "questions/create/blahblah")
        self.assertEqual(response.status_code, 404)


class ContestQuestionEditCreateUrlTest(TestCase):

    def setUp(self):
        self.createduser = User.objects.create_user(username="testnormaluser", email="testnormaluser@ts.com",
                                                    password="Test Hello World")
        self.contest = Contest.objects.create(author=self.createduser, title="Sample Question",
                                                short_description="Sample Short Desc", description="Sample Descrption",
                                                unique_code="sqdffe",start_date = "12/12/12",end_date="13/12/12",is_public=True,participants = self.createduser)

        self.question = Question.objects.create(author=self.createduser, title="Sample Question",
                                                short_description="Sample Short Desc", description="Sample Descrption",
                                                unique_code="sq")

        self.client = None
        self.request_url = '/contests/' + self.contest.unique_code+ + "/questions/" + self.question.unique_code +"/edit"
        # Create clients on the fly in the tests as login/logout is required

    def test_anonymous_ping(self):
        self.client = Client()
        response = self.client.get(self.request_url)

        #self.assertEqual(response.status_code,200)
        self.assertRedirects(response, expected_url="/registration/login?next=" + self.request_url)

    def test_authenticated_ping(self):
        self.client = Client()
        self.client.force_login(self.createduser)
        response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)

    def test_authenticated_random_id_ping(self):
        self.client = Client()
        self.client.force_login(self.createduser)
        response = self.client.get( '/contests/' + self.contest.unique_code+ + "/questions/" + self.question.unique_code +"/edit/blahblah")
        self.assertEqual(response.status_code, 404)


class ContestQuestionEditCreateUrlTest(TestCase):

    def setUp(self):
        self.createduser = User.objects.create_user(username="testnormaluser", email="testnormaluser@ts.com",
                                                    password="Test Hello World")
        self.contest = Contest.objects.create(author=self.createduser, title="Sample Question",
                                                short_description="Sample Short Desc", description="Sample Descrption",
                                                unique_code="sqdffe",start_date = "12/12/12",end_date="13/12/12",is_public=True,participants = self.createduser)


        self.client = None
        self.request_url = '/contests/' + self.contest.unique_code+ + "/view"
        # Create clients on the fly in the tests as login/logout is required

    def test_anonymous_ping(self):
        self.client = Client()
        response = self.client.get(self.request_url)

        #self.assertEqual(response.status_code,200)
        self.assertRedirects(response, expected_url="/registration/login?next=" + self.request_url)

    def test_authenticated_ping(self):
        self.client = Client()
        self.client.force_login(self.createduser)
        response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)

    def test_authenticated_random_id_ping(self):
        self.client = Client()
        self.client.force_login(self.createduser)
        response = self.client.get( '/contests/' + self.contest.unique_code + "/view/b;ahblah")
        self.assertEqual(response.status_code, 404)

