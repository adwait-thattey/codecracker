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
    def __init__(self, thread_id, testcase, code_file ):
        super().__init__()
        self.id = thread_id
        self.code = code_file
        self.testcase = testcase
        dir = os.path.dirname(code_file)
        self.error = os.path.join(dir, str(testcase.id), "error.txt")
        self.output = os.path.join(dir, str(testcase.id), "output.txt")
        self.result_code = -1


    def runcode(self):
        fi = open(self.code, mode="r")
        fo = open(self.output, mode="w")
        fe = open(self.error, mode="w")

        code_result = subprocess.run(["python3", self.code], stdin=fi, stdout=fo, stderr=fe)

        self.result_code = code_result.returncode

        if code_result.returncode == 0:
            print(str(self.id) + "completed successful execution")
        else:
            print(str(self.id) + "ran into an error")

        fi.close()
        fo.close()
        fe.close()
