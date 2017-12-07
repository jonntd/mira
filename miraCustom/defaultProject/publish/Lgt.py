# -*- coding: utf-8 -*-
import logging
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import open_file, quit_maya, save_as
from miraLibs.pipeLibs.pipeMaya import publish


def main(file_name, local):
    logger = logging.getLogger("Lgt publish")
    if not local:
        open_file.open_file(file_name)
    # get paths
    context = pipeFile.PathDetails.parse_path(file_name)
    # copy image and video
    publish.copy_image_and_video(context)
    logger.info("copy image and video done.")
    # copy to publish path
    save_as.save_as(context.publish_path)
    logger.info("Save to publish path.")
    # quit maya
    if not local:
        quit_maya.quit_maya()
