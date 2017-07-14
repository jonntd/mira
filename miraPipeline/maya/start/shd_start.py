# -*- coding: utf-8 -*-
import os
import logging
import optparse
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import new_file, save_as, create_reference, quit_maya


def main():
    logger = logging.getLogger("shd start")
    context = pipeFile.PathDetails.parse_path(options.file)
    project = context.project
    entity_type = context.entity_type
    asset_type = context.asset_type
    asset_name = context.asset_name
    mdl_publish_file = pipeFile.get_asset_task_publish_file(project, entity_type, asset_type, asset_name, "HighMdl", "HighMdl")
    if not os.path.isfile(mdl_publish_file):
        logger.warning("No model file published.")
        quit_maya.quit_maya()
        return
    new_file.new_file()
    create_reference.create_reference(mdl_publish_file)
    save_as.save_as(options.file)
    logger.info("%s publish successful!" % options.file)
    quit_maya.quit_maya()


if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-f", dest="file", help="maya file ma or mb.", metavar="string")
    parser.add_option("-c", dest="command",
                      help="Not a needed argument, just for mayabatch.exe, " \
                           "if missing this setting, optparse would " \
                           "encounter an error: \"no such option: -c\"",
                      metavar="string")
    options, args = parser.parse_args()
    if len([i for i in ["file_name"] if i in dir()]) == 1:
        options.file = file_name
        main()
