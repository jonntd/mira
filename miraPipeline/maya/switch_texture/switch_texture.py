# -*- coding: utf-8 -*-
import os
import pymel.core as pm
from miraLibs.mayaLibs import get_selected_group_sg
from miraLibs.mayaLibs import get_shader_history_nodes


def get_dst_path(src, mode="half"):
    dst_path = None
    dir_name, basename = os.path.split(src)
    if mode == "half":
        if dir_name.endswith("half"):
            return
        dst_path = "%s/half/%s" % (dir_name, basename)
    else:
        if dir_name.endswith("half"):
            dst_path = "%s/%s" % (os.path.dirname(dir_name), basename)
    return dst_path


def get_nodes(type_):
    """
    Ensure an iterable is returned even if no nodes exist in the scene.
    :param type_: str() - expecting a node type
    :return: list() of zero to N nodes of type_
    """
    sg_nodes = get_selected_group_sg.get_selected_group_sg()
    if not sg_nodes:
        return
    all_history_nodes = list()
    for sg_node in sg_nodes:
        history_nodes = get_shader_history_nodes.get_shader_history_nodes(sg_node)
        all_history_nodes.extend(history_nodes)
    all_history_nodes = list(set(all_history_nodes))
    nodes = [pm.PyNode(node) for node in all_history_nodes if pm.PyNode(node).type() == type_]
    return nodes


def switch_node_texture(type_, mode):
    """
    Based on the type_ passed in repath the current texture type with a new one.
    :param type_: string representing which texture type to access.
    :param mode: ??
    :return:
    """
    types = {"file": "fileTextureName",
             "RedshiftNormalMap": "tex0"}

    for node in get_nodes(type_):
        # obtain the attribute as chosen from types{}
        texture_node = getattr(node, types[type_])

        old_texture_name = texture_node.get()
        new_texture_name = get_dst_path(old_texture_name, mode)

        if new_texture_name:
            texture_node.set(new_texture_name)


def switch_texture(mode):
    switch_node_texture("file", mode)
    switch_node_texture("RedshiftNormalMap", mode)
