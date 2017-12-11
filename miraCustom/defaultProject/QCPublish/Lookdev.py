# -*- coding: utf-8 -*-
import os
import logging
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import save_as


def main():
    logger = logging.getLogger(__name__)
    # copy to QCPublish path
    context = pipeFile.PathDetails.parse_path()
    work_path = context.work_path
    if os.path.isfile(work_path):
        raise RuntimeError("File exist. Permission defined.")
    else:
        save_as.save_as(work_path)
        logger.info("Save to %s done." % work_path)
