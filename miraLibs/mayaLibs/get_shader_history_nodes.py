# -*- coding: utf-8 -*-
import maya.cmds as mc


def get_shader_history_nodes(node):
    if not mc.objExists(node):
        print "%s is not an exist node"
        return
    history_nodes = mc.listHistory(node, ac=1)
    history_nodes = list(set(history_nodes))
    return history_nodes
