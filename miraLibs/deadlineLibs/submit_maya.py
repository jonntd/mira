# -*- coding: utf-8 -*-
import os
import sys
import pymel.core as pm
import maya.mel as mel
import DeadlineSubmission
reload(DeadlineSubmission)
from DeadlineSubmission import DeadlineSubmission
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import get_render_images_dir


def submit_maya():
    context = pipeFile.PathDetails.parse_path(pm.sceneName())
    output_file_path = context.render_output
    # this will submit a job to deadline with the current maya scene's settings. It's just a placeholder at the moment
    # until we get our GUI up and running with this style of command line submission.
    driver, suffix = os.path.splitdrive(pm.sceneName())
    filein = "R:%s" % suffix
    mel.eval('setMayaSoftwareFrameExt(3,0);')
    pm.saveFile(f=1)
    filein_dir = os.path.dirname(filein)
    if not os.path.isdir(filein_dir):
        os.makedirs(filein_dir)
    pm.saveAs(filein)
    submit(filein, output_file_path)


def submit(filein=None, output_file_path=None):
    # dets = pft.PathDetails.parse_path(pm.sceneName())
    # fileout = dets.getRenderFullPath().split('.####.')[0]
    # pm.setAttr('defaultRenderGlobals.imageFilePrefix', fileout)
    if not filein:
        filein = pm.sceneName()
    if not output_file_path:
        output_file_path = get_render_images_dir.get_render_images_dir()
    maya_dir = os.path.dirname(sys.executable)
    maya_exex = '%s\Render.exe' % maya_dir
    start_frame = int(pm.playbackOptions(animationStartTime=True, query=True))
    end_frame = int(pm.playbackOptions(animationEndTime=True, query=True))
    name = os.path.basename(filein)
    # comment = ''
    maya_args = '-s <STARTFRAME>  -e <ENDFRAME>  -rd %s %s ' % (output_file_path, filein)

    sub = DeadlineSubmission()
    sub.setExe(maya_exex)
    sub.setArgs(maya_args)
    sub.setName(name)
    sub.setFrames("%s-%s" % (start_frame, end_frame))
    sub.setChunkSize(1)
    sub.submit()

