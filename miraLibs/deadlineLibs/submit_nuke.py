# -*- coding: utf-8 -*-
import os
import sys
from getpass import getuser
import pipeGlobal
import DeadlineSubmission
reload(DeadlineSubmission)
from DeadlineSubmission import DeadlineSubmission


def get_render_py():
    lib_dir = pipeGlobal.libs_dir
    render_py = "%s/pipeLibs/pipeNuke/render.py" % lib_dir
    return render_py


def submit_nuke():
    import nuke
    filein = nuke.root().name()
    job_name = "Nuke -- %s" % os.path.basename(filein)
    # dets = pft.PathDetails.parse_path(pm.sceneName())
    # fileout = dets.getRenderFullPath().split('.####.')[0]
    # pm.setAttr('defaultRenderGlobals.imageFilePrefix', fileout)
    nuke_exe = sys.executable
    # comment = ''
    render_py = get_render_py()
    submit(nuke_exe, filein, render_py, job_name)
    nuke.message("Submit Done.")


def submit(nuke_exe, filein, render_py, job_name):
    nuke_args = '-t %s %s' % (render_py, filein)
    sub = DeadlineSubmission()
    sub.setUserName(getuser())
    sub.setExe(nuke_exe)
    sub.setArgs(nuke_args)
    sub.setName(job_name)
    sub.setChunkSize(1)
    sub.submit()
