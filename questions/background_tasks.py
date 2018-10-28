import threading
import subprocess
from .models import TestCase
import os


def run_in_background(func):
    def decorator(*args, **kwargs):
        t = threading.Thread(target=func, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()

    return decorator


class RunAndAssert(threading.Thread):
    def __init__(self, thread_id, result_instance):
        super().__init__()
        self.result = result_instance
        self.id = thread_id
        self.code = result_instance.submission.code.path
        # self.self.result.testcase = self.result.testcase
        dir = os.path.dirname(self.code)
        dir = os.path.join(dir, str(self.result.testcase.id))

        if not os.path.exists(dir):
            os.makedirs(dir)

        self.error = os.path.join(dir, "error.txt")
        self.output = os.path.join(dir, "output.txt")
        self.result_code = -1

    def runcode(self):
        fi = open(self.code, mode="r")
        fo = open(self.output, mode="w")
        fe = open(self.error, mode="w")

        try:
            code_result = subprocess.run(["python3", self.code], stdin=fi, stdout=fo, stderr=fe, timeout=1)
            if code_result.returncode!=0:
                self.result_code = -1

        except subprocess.TimeoutExpired:
            self.result_code = -5

        #TODO Set timeout

        fi.close()
        fo.close()
        fe.close()

    def run(self):
        self.runcode()

        if self.result_code == 0:
            self.result.pass_fail = 1

        elif self.result_code == -1:
            fe = open(self.error, mode="r")
            self.result.pass_fail = 3
            self.result.errors = fe.read()
            fe.close()

        elif self.result_code == -5:
            self.result.pass_fail = 2

        else:
            raise ValueError("Unknown value of result_code")

        self.result.save()
