from django.contrib.auth.models import User
from django.test import TestCase
from contests.forms import *
from contests.models import *


class TestContestForm(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="testuser002", email="testuser002@ts.com", password="Hello World")

    def test_all_details_submitted(self):
        form_instance = HostContestForm(data={
            'title': "sample title",
            'unique_code': "testcode",
            'start_date': 12/12/2018,
            'start_time': "***",
            'end_date' : 13/12/2018,
            'end_time' : "****",
            'short_description' : "sample short des",
            'description' : "sample des",
            'eligibility' : "sample elig",
            'rules' : "sample rules",
            'prizes' : "sample prizes",
            'contacts' : "sample contacts",
            'is_public' : True,
            'registration_link' : "contests/create"
        })

        contest = form_instance.save(commit=False)

        contest.save()

        model_instance = Contest.objects.get(unique_code="testcode")

        self.assertEqual(model_instance.title, "sample title")
        self.assertEqual(model_instance.unique_code, "testcode")
        self.assertEqual(model_instance.start_date, 12/12/2018)
        self.assertEqual(model_instance.end_date, 13/12/2018)
        self.assertEqual(model_instance.start_time, "***")
        self.assertEqual(model_instance.end_time, "***")
        self.assertEqual(model_instance.short_description, "sample short des")
        self.assertEqual(model_instance.description, "sample des")
        self.assertEqual(model_instance.eligibility, "sample elig")
        self.assertEqual(model_instance.rules, "sample rules")
        self.assertEqual(model_instance.prizes, "sample prizes")
        self.assertEqual(model_instance.contacts, "sample contacts")
        self.assertEqual(model_instance.is_public, True)
        self.assertEqual(model_instance.registration_link, "contests/create")


    def test_missing_title(self):
        form_instance = HostContestForm(data={
            'unique_code': "testcode",
            'start_date': 12 / 12 / 2018,
            'start_time': "***",
            'end_date': 13 / 12 / 2018,
            'end_time': "****",
            'short_description': "sample short des",
            'description': "sample des",
            'eligibility': "sample elig",
            'rules': "sample rules",
            'prizes': "sample prizes",
            'contacts': "sample contacts",
            'is_public': True,
            'registration_link': "contests/create"
        })

        self.assertNotEqual(form_instance.errors.get("title"), None)



    def test_missing_unique_code(self):
        form_instance = HostContestForm(data={
            'title':'sample title',
            'start_date': 12 / 12 / 2018,
            'start_time': "***",
            'end_date': 13 / 12 / 2018,
            'end_time': "****",
            'short_description': "sample short des",
            'description': "sample des",
            'eligibility': "sample elig",
            'rules': "sample rules",
            'prizes': "sample prizes",
            'contacts': "sample contacts",
            'is_public': True,
            'registration_link': "contests/create"
        })

        self.assertNotEqual(form_instance.errors.get("unique_code"), None)

    def test_missing_start_date(self):
        form_instance = HostContestForm(data={
            'title':'sample title',
            'unique_code':"testcode",
            'start_time': "***",
            'end_date': 13 / 12 / 2018,
            'end_time': "****",
            'short_description': "sample short des",
            'description': "sample des",
            'eligibility': "sample elig",
            'rules': "sample rules",
            'prizes': "sample prizes",
            'contacts': "sample contacts",
            'is_public': True,
            'registration_link': "contests/create"
        })

        self.assertNotEqual(form_instance.errors.get("start"), None)

    def test_missing_start_time(self):
        form_instance = HostContestForm(data={
            'title':'sample title',
            'start_date': 12 / 12 / 2018,
            'unique_code':"testcode",
            'end_date': 13 / 12 / 2018,
            'end_time': "****",
            'short_description': "sample short des",
            'description': "sample des",
            'eligibility': "sample elig",
            'rules': "sample rules",
            'prizes': "sample prizes",
            'contacts': "sample contacts",
            'is_public': True,
            'registration_link': "contests/create"
        })

        self.assertEqual(form_instance.errors.get("start_time"), None)

    def test_missing_end_date(self):
        form_instance = HostContestForm(data={
            'title':'sample title',
            'start_date': 12 / 12 / 2018,
            'start_time': "***",
            'unique_code':"testcode",
            'end_time': "****",
            'short_description': "sample short des",
            'description': "sample des",
            'eligibility': "sample elig",
            'rules': "sample rules",
            'prizes': "sample prizes",
            'contacts': "sample contacts",
            'is_public': True,
            'registration_link': "contests/create"
        })

        self.assertNotEqual(form_instance.errors.get("end_date"), None)


    def test_missing_end_time(self):
        form_instance = HostContestForm(data={
            'title':'sample title',
            'start_date': 12 / 12 / 2018,
            'start_time': "***",
            'end_date': 13 / 12 / 2018,
            'end_time':"***",
            'short_description': "sample short des",
            'description': "sample des",
            'eligibility': "sample elig",
            'rules': "sample rules",
            'prizes': "sample prizes",
            'contacts': "sample contacts",
            'is_public': True,
            'registration_link': "contests/create"
        })

        self.assertEqual(form_instance.errors.get("end_time"), None)


    def test_missing_short_description(self):
        form_instance = HostContestForm(data={
            'title':'sample title',
            'start_date': 12 / 12 / 2018,
            'start_time': "***",
            'end_date': 13 / 12 / 2018,
            'end_time': "****",
            'unique_code':"testcode",
            'description': "sample des",
            'eligibility': "sample elig",
            'rules': "sample rules",
            'prizes': "sample prizes",
            'contacts': "sample contacts",
            'is_public': True,
            'registration_link': "contests/create"
        })

        self.assertNotEqual(form_instance.errors.get("short_description"), None)

    def test_missing_description(self):
        form_instance = HostContestForm(data={
            'title':'sample title',
            'start_date': 12 / 12 / 2018,
            'start_time': "***",
            'end_date': 13 / 12 / 2018,
            'end_time': "****",
            'short_description': "sample short des",
            'unique_code': "testcode",
            'eligibility': "sample elig",
            'rules': "sample rules",
            'prizes': "sample prizes",
            'contacts': "sample contacts",
            'is_public': True,
            'registration_link': "contests/create"
        })

        self.assertNotEqual(form_instance.errors.get("description"), None)

    def test_missing_eligibility(self):
        form_instance = HostContestForm(data={
            'title':'sample title',
            'start_date': 12 / 12 / 2018,
            'start_time': "***",
            'end_date': 13 / 12 / 2018,
            'end_time': "****",
            'short_description': "sample short des",
            'description': "sample des",
            'unique_code': "testcode",
            'rules': "sample rules",
            'prizes': "sample prizes",
            'contacts': "sample contacts",
            'is_public': True,
            'registration_link': "contests/create"
        })

        self.assertEqual(form_instance.errors.get("eligibility"), None)


    def test_missing_rules(self):
        form_instance = HostContestForm(data={
            'title':'sample title',
            'start_date': 12 / 12 / 2018,
            'start_time': "***",
            'end_date': 13 / 12 / 2018,
            'end_time': "****",
            'short_description': "sample short des",
            'description': "sample des",
            'eligibility': "sample elig",
            'unique_code': "testcode",
            'prizes': "sample prizes",
            'contacts': "sample contacts",
            'is_public': True,
            'registration_link': "contests/create"
        })

        self.assertEqual(form_instance.errors.get("rules"), None)


    def test_missing_prizes(self):
        form_instance = HostContestForm(data={
            'title':'sample title',
            'start_date': 12 / 12 / 2018,
            'start_time': "***",
            'end_date': 13 / 12 / 2018,
            'end_time': "****",
            'short_description': "sample short des",
            'description': "sample des",
            'eligibility': "sample elig",
            'rules': "sample rules",
            'unique_code': "testcode",
            'contacts': "sample contacts",
            'is_public': True,
            'registration_link': "contests/create"
        })

        self.assertEqual(form_instance.errors.get("prizes"), None)


    def test_missing_contacts(self):
        form_instance = HostContestForm(data={
            'title':'sample title',
            'start_date': 12 / 12 / 2018,
            'start_time': "***",
            'end_date': 13 / 12 / 2018,
            'end_time': "****",
            'short_description': "sample short des",
            'description': "sample des",
            'eligibility': "sample elig",
            'rules': "sample rules",
            'prizes': "sample prizes",
            'unique_code': "testcode",
            'is_public': True,
            'registration_link': "contests/create"
        })

        self.assertEqual(form_instance.errors.get("contacts"), None)


    def test_missing_is_public(self):
        form_instance = HostContestForm(data={
            'title':'sample title',
            'start_date': 12 / 12 / 2018,
            'start_time': "***",
            'end_date': 13 / 12 / 2018,
            'end_time': "****",
            'short_description': "sample short des",
            'description': "sample des",
            'eligibility': "sample elig",
            'rules': "sample rules",
            'prizes': "sample prizes",
            'contacts': "sample contacts",
            'unique_code': "testcode",
            'registration_link': "contests/create"
        })

        self.assertNotEqual(form_instance.errors.get("is_public"), None)


    def test_missing_registration_link(self):
        form_instance = HostContestForm(data={
            'title':'sample title',
            'start_date': 12 / 12 / 2018,
            'start_time': "***",
            'end_date': 13 / 12 / 2018,
            'end_time': "****",
            'short_description': "sample short des",
            'description': "sample des",
            'eligibility': "sample elig",
            'rules': "sample rules",
            'prizes': "sample prizes",
            'contacts': "sample contacts",
            'is_public': True,
            'unique_code': "testcode"
        })

        self.assertEqual(form_instance.errors.get("registration_link"), None)



class TestContestForm(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="testuser002", email="testuser002@ts.com", password="Hello World")

    def test_all_details_submitted(self):
        form_instance = ContestQuestionForm(data={
            "points" : 20
        })

        contestForm = form_instance.save(commit=False)

        contestForm.save()

        model_instance = Contest.objects.get(unique_code="testcode")

        self.assertEqual(model_instance.points, 20)