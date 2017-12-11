# -*- coding: utf-8 -*-
import maya.cmds as mc
from miraLibs.mayaLibs import get_all_parent_nodes
from miraLibs.pipeLibs import pipeFile
from miraLibs.pipeLibs.pipeMaya.shd import assign_shader
from Qt.QtWidgets import *
from Qt.QtCore import *


def get_model_groups():
    model_groups = list()
    for mesh in mc.ls(type="mesh"):
        sg_nodes = mc.listConnections(mesh, s=0, d=1, type="shadingEngine")
        if sg_nodes:
            continue
        parent_nodes = get_all_parent_nodes.get_all_parent_nodes(mesh, full_path=1)
        for parent_node in parent_nodes:
            if parent_node.endswith("_MODEL"):
                model_groups.append(parent_node)
    model_groups = list(set(model_groups))
    return model_groups


def fix_shader():
    model_groups = get_model_groups()
    if not model_groups:
        return
    progress_dialog = QProgressDialog('Correcting shader,Please wait......', 'Cancel', 0, len(model_groups))
    progress_dialog.setWindowModality(Qt.WindowModal)
    progress_dialog.setMinimumWidth(300)
    progress_dialog.show()
    for index, model_group in enumerate(model_groups):
        if progress_dialog.wasCanceled():
            break
        asset_name = model_group.split("|")[-1].split("_")[1]
        for ref_file in mc.file(q=1, r=1):
            try:
                context = pipeFile.PathDetails.parse_path(ref_file.replace("CProp", "Cprop"))
                if context.asset_name == asset_name and context.area == "_shd":
                    mc.file(ref_file, rr=1)
                    assign_shader.assign_shader(model_group)
            except Exception as e:
                print e
        progress_dialog.setValue(index + 1)
