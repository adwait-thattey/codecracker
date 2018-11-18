
from django.test import Client, TestCase
from django.contrib.auth.models import User
from questions.models import Question


# TODO Set tests for logged in users, having different configurations like with and without more_user_data
# Check out the client login method https://docs.djangoproject.com/en/2.1/topics/testing/tools/#django.test.Client.login
# Check this request factory method out for above : https://docs.djangoproject.com/en/2.1/topics/testing/advanced/#example

class SubmitSolutionUrlTest(TestCase):

    def setUp(self):
        self.createduser = User.objects.create_user(username="testnormaluser", email="testnormaluser@ts.com",
                                                    password="Test Hello World")
        self.question = Question.objects.create(author=self.createduser, title="Sample Question",
                                                short_description="Sample Short Desc", description="Sample Descrption",
                                                unique_code="sq")
        self.client = None
        self.request_url = '/questions/' + self.question.unique_code + "/submit"
        # Create clients on the fly in the tests as login/logout is required

    def test_anonymous_ping(self):
        self.client = Client()
        response = self.client.get(self.request_url)

        self.assertRedirects(response, expected_url="/registration/login?next=" + self.request_url)

    def test_authenticated_ping(self):
        self.client = Client()
        self.client.force_login(self.createduser)
        response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)

    def test_authenticated_random_id_ping(self):
        self.client = Client()
        self.client.force_login(self.createduser)
        response = self.client.get('/questions/blahblah/submit')
        self.assertEqual(response.status_code, 404)
class QuestionBrowseUrlTest(TestCase):

    def setUp(self):
        self.createduser = User.objects.create_user(username="testnormaluser", email="testnormaluser@ts.com",
                                                    password="Test Hello World")
        self.question = Question.objects.create(author=self.createduser, title="Sample Question",
                                                short_description="Sample Short Desc", description="Sample Descrption",
                                                unique_code="sq")
        self.client = None
        self.request_url = '/questions/browse'
        # Create clients on the fly in the tests as login/logout is required

    def test_anonymous_ping(self):
        self.client = Client()
        response = self.client.get(self.request_url)

        self.assertEqual(response.status_code,200)


    def test_authenticated_random_id_ping(self):
        self.client = Client()
        self.client.force_login(self.createduser)
        response = self.client.get('/questions/blahblah/submit')
        self.assertEqual(response.status_code, 404) 
             
class QuestionPostUrlTest(TestCase):

    def setUp(self):
        self.createduser = User.objects.create_user(username="testnormaluser", email="testnormaluser@ts.com",
                                                    password="Test Hello World")
        self.question = Question.objects.create(author=self.createduser, title="Sample Question",
                                                short_description="Sample Short Desc", description="Sample Descrption",
                                                unique_code="sq")
        self.client = None
        self.request_url = '/questions/post/'
        # Create clients on the fly in the tests as login/logout is required

    def test_anonymous_ping(self):
        self.client = Client()
        response = self.client.get(self.request_url)

        self.assertRedirects(response, expected_url="/registration/login?next=" + self.request_url)

    
    def test_authenticated_ping(self):
        self.client = Client()
        self.client.force_login(self.createduser)
        response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)      


    def test_authenticated_random_id_ping(self):
        self.client = Client()
        self.client.force_login(self.createduser)
        response = self.client.get('/questions/blahblah/post/')
        self.assertEqual(response.status_code, 404)        
class ViewQuestion(TestCase):

    def setUp(self):
        self.createduser = User.objects.create_user(username="testnormaluser", email="testnormaluser@ts.com",
                                                    password="Test Hello World")
        self.question = Question.objects.create(author=self.createduser, title="Sample Question",
                                                short_description="Sample Short Desc", description="Sample Descrption",
                                                unique_code="sq")
        self.client = None
        self.request_url = '/questions/' + self.question.unique_code + "/view/"
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
        response = self.client.get('/questions/blahblah/view/')
        self.assertEqual(response.status_code, 404)        
class TestCaseView(TestCase):

    def setUp(self):
        self.createduser = User.objects.create_user(username="testnormaluser", email="testnormaluser@ts.com",
                                                    password="Test Hello World")
        self.question = Question.objects.create(author=self.createduser, title="Sample Question",
                                                short_description="Sample Short Desc", description="Sample Descrption",
                                                unique_code="sq")
        self.client = None
        self.request_url = '/questions/' + self.question.unique_code + '/testcases/view'
        # Create clients on the fly in the tests as login/logout is required

    def test_anonymous_ping(self):
        self.client = Client()
        response = self.client.get(self.request_url)
        self.assertRedirects(response, expected_url="/registration/login?next=" + self.request_url)
    def test_authenticated_ping(self):
        self.client = Client()
        self.client.force_login(self.createduser)
        response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
    
    def test_authenticated_random_id_ping(self):
        self.client = Client()
        self.client.force_login(self.createduser)
        response = self.client.get('/questions/blahblah/testcases/view')
        self.assertEqual(response.status_code, 404)        
class TestCaseNew(TestCase):

    def setUp(self):
        self.createduser = User.objects.create_user(username="testnormaluser", email="testnormaluser@ts.com",
                                                    password="Test Hello World")
        self.question = Question.objects.create(author=self.createduser, title="Sample Question",
                                                short_description="Sample Short Desc", description="Sample Descrption",
                                                unique_code="sq")
        self.client = None
        self.request_url = '/questions/' + self.question.unique_code + '/testcases/new'
        # Create clients on the fly in the tests as login/logout is required

    def test_anonymous_ping(self):
        self.client = Client()
        response = self.client.get(self.request_url)
        self.assertRedirects(response, expected_url="/registration/login?next=" + self.request_url)
    def test_authenticated_ping(self):
        self.client = Client()
        self.client.force_login(self.createduser)
        response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)
    
    def test_authenticated_random_id_ping(self):
        self.client = Client()
        self.client.force_login(self.createduser)
        response = self.client.get('/questions/blahblah/testcases/new')
        self.assertEqual(response.status_code, 404) 
class SubmissionResultUrlTest(TestCase):

    def setUp(self):
        self.createduser = User.objects.create_user(username="testnormaluser", email="testnormaluser@ts.com",
                                                    password="Test Hello World")
        self.question = Question.objects.create(author=self.createduser, title="Sample Question",
                                                short_description="Sample Short Desc", description="Sample Descrption",
                                                unique_code="sq")
        
        self.client = None
        self.request_url = '/questions/ajax/submission-result'
        # Create clients on the fly in the tests as login/logout is required

    def test_no_submission_anonymous_ping(self):
        self.client = Client()
        response = self.client.get(self.request_url)

        self.assertEqual(response.status_code,404)

    
    def test_no_submission_authenticated_ping(self):
        self.client = Client()
        self.client.force_login(self.createduser)
        response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 404)      


    #TODO Make Post Request Submission tests
       
# class TestCase(TestCase):

#     def setUp(self):
#         self.createduser = User.objects.create_user(username="testnormaluser", email="testnormaluser@ts.com",
#                                                     password="Test Hello World")
#         self.question = Question.objects.create(author=self.createduser, title="Sample Question",
#                                                 short_description="Sample Short Desc", description="Sample Descrption",
#                                                 unique_code="sq")
#         self.client = None
#         self.request_url = '/questions/' + self.question.unique_code + '/testcases'
#         # Create clients on the fly in the tests as login/logout is required

#     def test_anonymous_ping(self):
#         self.client = Client()
#         response = self.client.get(self.request_url)
#         self.assertRedirects(response, expected_url = self.request_url + "view", target_status_code=301)
    
    # def test_authenticated_ping(self):
    #     self.client = Client()
    #     self.client.force_login(self.createduser)
    #     response = self.client.get(self.request_url)
    #     self.assertEqual(response.status_code, 200)
    # 