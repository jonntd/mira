# -*- coding: utf-8 -*-
import os
import sys
from getpass import getuser
import DeadlineSubmission
reload(DeadlineSubmission)
from DeadlineSubmission import DeadlineSubmission
from miraLibs.pipeLibs import pipeFile


def submit_maya():
    import pymel.core as pm
    import maya.mel as mel

    context = pipeFile.PathDetails.parse_path(pm.sceneName())
    output_file_path = context.render_output

    maya_dir = os.path.dirname(sys.executable)
    maya_exe = '%s\Render.exe' % maya_dir

    start_frame = int(pm.playbackOptions(animationStartTime=True, query=True))
    end_frame = int(pm.playbackOptions(animationEndTime=True, query=True))

    driver, suffix = os.path.splitdrive(pm.sceneName())
    filein = "R:%s" % suffix
    job_name = "Maya -- %s" % os.path.basename(filein)
    mel.eval('setMayaSoftwareFrameExt(3,0);')
    pm.saveFile(f=1)
    filein_dir = os.path.dirname(filein)
    if not os.path.isdir(filein_dir):
        os.makedirs(filein_dir)
    pm.saveAs(filein)
    submit(maya_exe, filein, output_file_path, start_frame, end_frame, job_name)


def submit(maya_exe, filein, output_file_path, start, end, job_name):
    # dets = pft.PathDetails.parse_path(pm.sceneName())
    # fileout = dets.getRenderFullPath().split('.####.')[0]
    # pm.setAttr('defaultRenderGlobals.imageFilePrefix', fileout)
    # comment = ''
    maya_args = '-s <STARTFRAME>  -e <ENDFRAME>  -rd %s %s ' % (output_file_path, filein)
    sub = DeadlineSubmission()
    sub.setUserName(getuser())
    sub.setExe(maya_exe)
    sub.setArgs(maya_args)
    sub.setName(job_name)
    sub.setFrames("%s-%s" % (start, end))
    sub.setChunkSize(1)
    sub.submit()
