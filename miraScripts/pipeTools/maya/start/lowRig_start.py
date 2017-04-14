# -*- coding: utf-8 -*-
import os
import logging
import optparse
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import new_file, save_as, create_reference, create_group, quit_maya


def main():
    logger = logging.getLogger("lowRig start")
    obj = pipeFile.PathDetails.parse_path(options.file)
    project_name = obj.project
    asset_type = obj.asset_type
    asset_type_short_name = obj.asset_type_short_name
    asset_name = obj.asset_name
    mdl_publish_file = pipeFile.get_asset_step_publish_file(asset_type, asset_name, "lowMdl", project_name)
    if not os.path.isfile(mdl_publish_file):
        logger.warning("No model file published.")
        quit_maya.quit_maya()
        return
    new_file.new_file()
    create_reference.create_reference(mdl_publish_file)
    model_name = "%s_%s_MODEL" % (asset_type_short_name, asset_name)
    # create root group
    root_group_name = "%s_%s_ROOT" % (asset_type_short_name, asset_name)
    create_group.create_group(root_group_name)
    # create _BLENDS group
    blends_group = "_BLENDS"
    create_group.create_group(blends_group)
    if asset_type == "character":
        rig_group_name = "Grp_Master_Ctl"
        create_group.create_group("Others", root_group_name)
        create_group.create_group("Geometry", root_group_name)
        create_group.create_group(model_name, "Geometry")
    elif asset_type == "prop":
        rig_group_name = "%s_%s_RIG" % (asset_type_short_name, asset_name)
        create_group.create_group(model_name, root_group_name)
    create_group.create_group(rig_group_name, root_group_name)

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