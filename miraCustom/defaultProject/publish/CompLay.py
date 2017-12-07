# -*- coding: utf-8 -*-
import logging
import nuke
from miraLibs.pipeLibs import pipeFile
from miraLibs.pyLibs import copy


def copy_image_and_video(context):
    # copy image and video to publish
    work_image_path = context.work_image_path
    work_video_path = context.work_video_path
    image_path = context.image_path
    video_path = context.video_path
    copy.copy(work_image_path, image_path)
    copy.copy(work_video_path, video_path)


def main():
    logger = logging.getLogger(__name__)
    args = nuke.rawArgs
    file_name = args[3]
    context = pipeFile.PathDetails.parse_path(file_name)
    # copy image and video
    copy_image_and_video(context)
    logger.info("Copy image and video done.")
    # copy to publish
    publish_path = context.publish_path
    copy.copy(file_name, publish_path)
    logger.info("Copy to publish path.")


if __name__ == "__main__":
    main()
