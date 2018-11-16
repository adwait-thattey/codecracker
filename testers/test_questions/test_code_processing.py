import os

from django.conf.global_settings import MEDIA_ROOT
from django.contrib.auth.models import User
from django.test import Client, TestCase
import questions.models as models
from questions.background_tasks import RunAndAssert
from threading import Event


class CodeRunTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username="testuser",
                                        email="testuser@testers.com",
                                        password="Hello World")

        self.question = models.Question(author=self.user,
                                        title="Sample Title",
                                        description="Test Description",
                                        time_limit=3.0,
                                        unique_code="testq",
                                        )
        self.question.save()

        dir = os.path.join(MEDIA_ROOT, "code_tests")

        if not os.path.exists(dir):
            os.makedirs(dir)

        self.input_file = os.path.join("code_tests", "sample_input.txt")
        self.output_file = os.path.join("code_tests", "sample_output.txt")
        self.correct_code_file = os.path.join("code_tests", "correct_code.py")
        self.wrong_code_file = os.path.join("code_tests", "wrong_code.py")
        self.error_code_file = os.path.join("code_tests", "error_code.py")
        self.tle_code_file = os.path.join("code_tests", "tle_code.py")

        self.testcase = models.TestCase(question=self.question,
                                        number=1,
                                        input_file=self.input_file,
                                        output_file=self.output_file,
                                        points=10
                                        )
        self.testcase.save()

        self.correct_submission = models.Submission(question=self.question,
                                                    user=self.user,
                                                    language="PY3",
                                                    code=self.correct_code_file
                                                    )
        self.correct_submission.save()

        self.correct_result = models.Result(submission=self.correct_submission,
                                            testcase=self.testcase,
                                            )
        self.correct_result.save()

        self.wrong_submission = models.Submission(question=self.question,
                                                  user=self.user,
                                                  language="PY3",
                                                  code=self.wrong_code_file
                                                  )
        self.wrong_submission.save()

        self.wrong_result = models.Result(submission=self.wrong_submission,
                                          testcase=self.testcase,
                                          )
        self.wrong_result.save()

        self.error_submission = models.Submission(question=self.question,
                                                  user=self.user,
                                                  language="PY3",
                                                  code=self.error_code_file
                                                  )
        self.error_submission.save()

        self.error_result = models.Result(submission=self.error_submission,
                                          testcase=self.testcase,
                                          )
        self.error_result.save()

        self.tle_submission = models.Submission(question=self.question,
                                                user=self.user,
                                                language="PY3",
                                                code=self.tle_code_file
                                                )
        self.tle_submission.save()

        self.tle_result = models.Result(submission=self.tle_submission,
                                        testcase=self.testcase,
                                        )
        self.tle_result.save()

    def test_correct_code(self):

        code_runner = RunAndAssert(12, self.correct_result)
        code_runner.run()

        result = models.Result.objects.get(submission=self.correct_result.submission, testcase=self.correct_result.testcase)

        self.assertEqual(result.pass_fail, 1)

    def test_wrong_code(self):

        code_runner = RunAndAssert(12, self.wrong_result)
        code_runner.run()

        result = models.Result.objects.get(submission=self.wrong_result.submission, testcase=self.wrong_result.testcase)

        self.assertEqual(result.pass_fail, 4)

    def test_error_code(self):

        code_runner = RunAndAssert(12, self.error_result)
        code_runner.run()

        result = models.Result.objects.get(submission=self.error_result.submission, testcase=self.error_result.testcase)

        self.assertEqual(result.pass_fail, 3)

    def test_tle_code(self):

        code_runner = RunAndAssert(12, self.tle_result)
        code_runner.run()

        result = models.Result.objects.get(submission=self.tle_result.submission, testcase=self.tle_result.testcase)

        self.assertEqual(result.pass_fail, 2)