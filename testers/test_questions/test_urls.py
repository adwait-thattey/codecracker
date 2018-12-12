
from django.test import Client, TestCase
from django.contrib.auth.models import User
from questions.models import Question
#from questions.models import TestCase

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
       
'''class TestCase(TestCase):

    def setUp(self):
         self.createduser = User.objects.create_user(username="testnormaluser", email="testnormaluser@ts.com",
                                                     password="Test Hello World")
         self.question = Question.objects.create(author=self.createduser, title="Sample Question",
                                                 short_description="Sample Short Desc", description="Sample Descrption",
                                                 unique_code="sq")
         self.client = None
         #self.request_url = '/questions/' + self.question.unique_code + '/testcases/'
         # Create clients on the fly in the tests as login/logout is required

    def test_anonymous_ping(self):
         self.client = Client()
         response = self.client.post("/questions/sq/testcases/")
         self.assertEqual(response.status_code,302)

    
    def test_authenticated_ping(self):
         self.client = Client()
         self.client.force_login(self.createduser)
         response = self.client.post("/questions/sq/testcases/")
         self.assertRedirects(response, expected_url="/questions/sq/testcases/view")'''

class TestCaseSubmissionUrlTest(TestCase):

    def setUp(self):
        self.createduser = User.objects.create_user(username="testnormaluser", email="testnormaluser@ts.com",
                                                    password="Test Hello World")
        self.question = Question.objects.create(author=self.createduser, title="Sample Question",
                                                short_description="Sample Short Desc", description="Sample Descrption",
                                                unique_code="sq")
        self.client = None
        self.request_url = '/questions/ajax/rerun_test_case_submissions/' + self.question.unique_code 
        
        # Create clients on the fly in the tests as login/logout is required

    def test_anonymous_ping(self):
        self.client = Client()
        response = self.client.get(self.request_url)

        self.assertEquals(response.status_code,200)

    def test_authenticated_ping(self):
        self.client = Client()
        self.client.force_login(self.createduser)
        response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)

    def test_authenticated_random_id_ping(self):
        self.client = Client()
        self.client.force_login(self.createduser)
        response = self.client.get('/questions/ajax/rerun_test_case_submissions/')
        self.assertEqual(response.status_code, 404)
    
class EditUrlTest(TestCase):

    def setUp(self):
        self.createduser = User.objects.create_user(username="testnormaluser", email="testnormaluser@ts.com",
                                                    password="Test Hello World")
        self.question = Question.objects.create(author=self.createduser, title="Sample Question",
                                                short_description="Sample Short Desc", description="Sample Descrption",
                                                unique_code="sq")
        self.client = None
        self.request_url = '/questions/' + self.question.unique_code +'/edit'
        
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
class TestCaseDeleteUrlTest(TestCase):

    def setUp(self):
        self.createduser = User.objects.create_user(username="testnormaluser", email="testnormaluser@ts.com",
                                                    password="Test Hello World")
        self.question = Question.objects.create(author=self.createduser, title="Sample Question",
                                                short_description="Sample Short Desc", description="Sample Descrption",
                                                unique_code="sq")
        
        self.client = None
        
        
        #<slug:question_unique_id>/testcase/<int:test_case_number>/delete
        
        # Create clients on the fly in the tests as login/logout is required

    def test_anonymous_ping(self):
        self.client = Client()
        response = self.client.post("/questions/sq/testcase/4/delete")
        

        self.assertRedirects(response,expected_url="/registration/login?next=/questions/sq/testcase/4/delete")
    def no_test_authenticated_ping(self):
        self.client = Client()
        self.client.force_login(self.createduser)
        response = self.client.post("/questions/sq/testcase/4/delete")
        self.assertEqual(response.status_code, 200)

# class SubmissionResultUrlTest(TestCase):

#     def setUp(self):
#         self.createduser = User.objects.create_user(username="testnormaluser", email="testnormaluser@ts.com",
#                                                     password="Test Hello World")
#         self.question = Question.objects.create(author=self.createduser, title="Sample Question",
#                                                 short_description="Sample Short Desc", description="Sample Descrption",
#                                                 unique_code="sq",submission_count="0")
        
#         self.submission = Submission.objects.create()
#         self.client = None
#         self.request_url = '/questions/' + self.question.unique_code + '/' + self.createduser.username + '/submission/'+self. +'/result'
#         #<slug:question_unique_id>/submission/<int:submission_attempt>/result
        
#         # Create clients on the fly in the tests as login/logout is required

#     def test_anonymous_ping(self):
#         self.client = Client()
#         response = self.client.get(self.request_url)

#         self.assertRedirects(response, expected_url="/registration/login?next=" + self.request_url)
#     def test_authenticated_ping(self):
#         self.client = Client()
#         self.client.force_login(self.createduser)
#         response = self.client.get(self.request_url)
#         self.assertEqual(response.status_code, 200)'''
class TestCaseEditUrlTest(TestCase):

    def setUp(self):
        self.createduser = User.objects.create_user(username="testnormaluser", email="testnormaluser@ts.com",
                                                    password="Test Hello World")
        self.question = Question.objects.create(author=self.createduser, title="Sample Question",
                                                short_description="Sample Short Desc", description="Sample Descrption",
                                                unique_code="sq")
        
        self.client = None
        
        
    
        
        # Create clients on the fly in the tests as login/logout is required

    def test_anonymous_ping(self):
        self.client = Client()
        response = self.client.post("/questions/sq/testcase/4/edit")
        

        self.assertRedirects(response,expected_url="/registration/login?next=/questions/sq/testcase/4/edit")
    def no_test_authenticated_ping(self):
        self.client = Client()
        self.client.force_login(self.createduser)
        response = self.client.post("/questions/sq/testcase/4/edit")
        self.assertEqual(response.status_code, 404)

class UrlTest(TestCase):

    
    def test_anonymous_ping(self):
        self.client = Client()
        response = self.client.get('/questions/')

        self.assertRedirects(response,expected_url="/questions/browse")

 

    




    


