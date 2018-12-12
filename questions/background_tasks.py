import threading
import subprocess
import time
from collections import deque

from django.conf import settings
from django.urls import reverse

from registration.models import send_notification
from .docker import Docker
from django.db import connection

from .models import TestCase
import os

CURRENT_PARALLEL_THREADS = 0


class RunAndAssert(threading.Thread):
    def __init__(self, thread_id, result_instance, code_file=None):
        """

        :param thread_id: Give an id to the thread
        :param result_instance: An instance of the result model
        :param code_file: Provide this file if you are doing any pre-processing on user \
        submitted code. For ex. If user is giving code in c++, compile it in pre-processing\
         and pass the a.out file here.

        """
        super().__init__()
        self.result = result_instance
        self.id = thread_id

        if code_file is None:
            self.code = result_instance.submission.code.path
        else:
            self.code = code_file

        self.result_code = -1

        self.docker_instance = Docker(
            unique_code="cont" + str(self.result.id),
            code_file=self.code,
            input_file=self.result.testcase.input_file.path,
            time_limit=self.result.submission.question.time_limit
        )



    def run_code(self):

        # TODO Add support for more languages

        code_status = self.docker_instance.run_code_and_return_status()
        if code_status == 124:
            self.result_code = -5

        elif code_status == -1:
            self.result_code = -1

        else:
            self.result_code = 0


        # TODO Set timeout


    def assert_output(self):
        exp_output = self.result.testcase.output_file.path

        f1 = open(exp_output, mode="r")
        f2 = open(self.docker_instance.output_file, mode="r")

        result = False
        if f1.read() == f2.read():
            result = True

        f1.close()
        f2.close()

        return result

    def run(self):
        global CURRENT_PARALLEL_THREADS
        CURRENT_PARALLEL_THREADS += 1
        print(CURRENT_PARALLEL_THREADS)

        self.result.pass_fail = 5
        self.result.save()

        self.run_code()
        if self.result_code == 0:
            result = self.assert_output()
            if result:
                self.result.pass_fail = 1
            else:
                self.result.pass_fail = 4

        elif self.result_code == -1:
            fe = open(self.docker_instance.error_file, mode="r")
            self.result.pass_fail = 3
            self.result.errors = fe.read()
            fe.close()

        elif self.result_code == -5:
            self.result.pass_fail = 2

        else:
            raise ValueError("Unknown value of result_code")

        self.result.save()

        self.teardown()

    def teardown(self):
        self.docker_instance.delete_dir()
        # connection.close()
        global CURRENT_PARALLEL_THREADS
        CURRENT_PARALLEL_THREADS -= 1
        print(CURRENT_PARALLEL_THREADS)


class Scheduler(threading.Thread):
    def __init__(self, threadlist):
        super().__init__()
        self.threadlist = threadlist

    def run(self):
        th_pointer = 0
        while th_pointer < len(self.threadlist):
            if CURRENT_PARALLEL_THREADS < settings.CODE_THREAD_LIMIT:
                th = self.threadlist[th_pointer]
                th.start()
                th_pointer+=1

        for th in self.threadlist:
            th.join()


class RunAndReCalc(threading.Thread):
    def __init__(self, thread_id, result_instance, code_file=None):
        super().__init__()
        self.result = result_instance
        self.code_file = code_file
        self.thr_id = thread_id

    def run(self):
        thr = RunAndAssert(self.thr_id, self.result, self.code_file)
        thr.run()

        self.result.submission.recalc_score()


class LimitThreads(threading.Thread):
    def __init__(self, thread_id, thread_list):
        """

        :param thread_id:
        :param thread_list:
        """

        super().__init__()
        self.thread_id = thread_id
        self.thread_list = thread_list

    def run(self):
        # print("chunk start")
        for th in self.thread_list:
            th.start()

        for th in self.thread_list:
            th.join()

        # print("chunk end")


class ThreadRunner(threading.Thread):
    def __init__(self, thread_id, thread_list):
        super().__init__()
        self.thread_id = thread_id
        self.thread_list = thread_list

    def run(self):

        for th in self.thread_list:
            while CURRENT_PARALLEL_THREADS >= settings.CODE_THREAD_LIMIT:
                pass
            th.start()

        for th in self.thread_list:
            th.join()


class SubmissionRunnerController(threading.Thread):
    def __init__(self, thread_id, submission):
        super().__init__()
        self.thread_id = thread_id
        self.submission = submission

    def run(self):
        result_set = self.submission.result_set.all()
        thread_list = list()
        for R in result_set:
            thread_temp = RunAndAssert(thread_id=R.testcase.id, result_instance=R)
            thread_list.append(thread_temp)

        tr = ThreadRunner(self.thread_id + self.submission.id, thread_list)
        tr.run()

        self.submission.recalc_score()

        send_notification(user=self.submission.user,
                          content=f"submission for {self.submission.question.unique_code} has finished.",
                          link=reverse("questions:submission-result", args=[self.submission.question.unique_code, self.submission.user.username, self.submission.attempt_number ]),
                          icon="check"
                        )
