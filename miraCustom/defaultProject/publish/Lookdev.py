# -*- coding: utf-8 -*-
import logging
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import open_file, quit_maya, save_as
from miraLibs.pipeLibs.pipeMaya import publish


def main(file_name, local):
    logger = logging.getLogger("Lookdev publish")
    if not local:
        open_file.open_file(file_name)
    # get paths
    context = pipeFile.PathDetails.parse_path()
    publish.copy_image_and_video(context)
    logger.info("copy image and video done.")
    save_as.save_as(context.publish_path)
    # quit maya
    if not local:
        quit_maya.quit_maya()
