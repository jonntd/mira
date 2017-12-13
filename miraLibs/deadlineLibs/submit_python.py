# -*- coding: utf-8 -*-
from getpass import getuser
import pipeGlobal
import DeadlineSubmission
reload(DeadlineSubmission)
from DeadlineSubmission import DeadlineSubmission


def submit_python(py_path, args, white_list, job_name):
    python_exe = pipeGlobal.exe.get("python").get("py27").get("pythonbin")
    submit(python_exe, py_path, args=args, white_list=white_list, job_name=job_name)


def submit(python_exe, py_path, args, white_list, job_name):
    python_args = "%s %s" % (py_path, args)
    sub = DeadlineSubmission()
    sub.setUserName(getuser())
    sub.setExe(python_exe)
    sub.setArgs(python_args)
    sub.setWhiteList(white_list)
    sub.setName(job_name)
    sub.setChunkSize(1)
    sub.submit()
