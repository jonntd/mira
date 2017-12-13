# -*- coding: utf-8 -*-
from getpass import getuser
import pipeGlobal
import DeadlineSubmission
reload(DeadlineSubmission)
from DeadlineSubmission import DeadlineSubmission


def submit_python(py_path, args, white_list, job_name):
    submit("2.7", py_path, args=args, white_list=white_list, job_name=job_name)


def submit(python_version, py_path, args, white_list, job_name):
    python_args = "%s %s" % (py_path, args)
    sub = DeadlineSubmission()
    sub.setPlugin("Python")
    sub.setArgs(python_args)
    sub.setVersion(python_version)
    sub.setScriptFile(py_path)
    sub.setWhiteList(white_list)
    sub.setName(job_name)
    sub.setChunkSize(1)
    sub.submit()
