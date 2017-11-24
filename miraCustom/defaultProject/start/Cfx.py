# -*- coding: utf-8 -*-
import os
import logging
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import new_file, quit_maya, open_file
from miraLibs.pyLibs import copy


def main(file_name, local):
    logger = logging.getLogger("Cfx start")
    new_file.new_file()
    context = pipeFile.PathDetails.parse_path(file_name)
    project = context.project
    sequence = context.sequence
    shot = context.shot
    task = "Anim" if context.task == "Cfx" else context.task
    anim_publish_file = pipeFile.get_task_publish_file(project, "Shot", sequence, shot, "Anim", task)
    if not os.path.isfile(anim_publish_file):
        logger.warning("%s is not an exist file" % anim_publish_file)
        if local:
            return
        else:
            quit_maya.quit_maya()
    copy.copy(anim_publish_file, file_name)
    logger.info("copy %s to %s" % (anim_publish_file, file_name))
    if local:
        open_file.open_file(file_name)
    else:
        quit_maya.quit_maya()
