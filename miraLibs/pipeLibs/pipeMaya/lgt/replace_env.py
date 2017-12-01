# -*- coding: utf-8 -*-
import os
import logging
import maya.cmds as mc
from Qt.QtWidgets import *
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import export_abc, create_reference, save_as, Assembly


logger = logging.getLogger(__name__)


def check_no_shd_in_reps():
    no_shd = list()
    ar_nodes = mc.ls(type="assemblyReference")
    if not ar_nodes:
        return
    for ar_node in ar_nodes:
        reps = mc.assembly(ar_node, q=1, listRepresentations=1)
        if "MidMdl" in reps and "Shd" not in reps:
            no_shd.append(ar_node)
    if no_shd:
        message = "These assembly nodes has no Shd rep:\n%s" % "\n".join(no_shd)
        QMessageBox.warning(None, "Warming Tip", message)
        return True
    else:
        return False


def export_env_cache(cache_path):
    export_abc.export_abc(1, 1, cache_path, "Env")
    logger.info("Export env cache done.")


def import_env_cache(abc_path):
    if os.path.isfile(abc_path):
        create_reference.create_reference(abc_path)
        logger.info("Import env cache done.")
    else:
        logger.warning("No env cache exists.")


def main():
    if not mc.objExists("Env"):
        logger.info("Env group not exist.")
        return
    if check_no_shd_in_reps():
        return
    assemb = Assembly.Assembly()
    assemb.set_active("Shd")
    context = pipeFile.PathDetails.parse_path()
    cache_dir = context.cache_dir
    abc_path = "%s/env.abc" % cache_dir
    # export Env group as abc to cache dir
    export_env_cache(abc_path)
    # delete Env group
    mc.delete("Env")
    logger.info("Delete Env group done.")
    # import abc
    import_env_cache(abc_path)
    # save as next edition file
    next_edition_file = context.next_edition_file
    save_as.save_as(next_edition_file)
    logger.info("Save as next edition file done.")
