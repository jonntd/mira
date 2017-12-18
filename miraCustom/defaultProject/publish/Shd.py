# -*- coding: utf-8 -*-
import os
import logging
import maya.cmds as mc
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import open_file, quit_maya, export_selected, \
    delete_history, delete_unused_nodes, delete_layer, unlock_normal, \
    get_selected_group_sg, get_shader_history_nodes, remove_namespace, delete_intermediate_object
from miraLibs.pipeLibs.pipeMaya import rename_pipeline_shape, publish, get_model_name
from miraLibs.pyLibs.image import resize_image


def get_created_sg_node():
    exclude_sg = ["initialParticleSE", "initialShadingGroup"]
    sg_nodes = get_selected_group_sg.get_selected_group_sg()
    created_sg = list(set(sg_nodes)-set(exclude_sg))
    return created_sg


def get_prefix(context):
    asset_name = context.asset_name
    task = context.task
    prefix = asset_name+"_"+task+"_"
    return prefix


def rename_shd_mat_node(context):
    prefix = get_prefix(context)
    created_sg = get_created_sg_node()
    if not created_sg:
        return
    for sg in created_sg:
        material_nodes = get_shader_history_nodes.get_shader_history_nodes(sg)
        for node in material_nodes:
            if node.startswith(prefix):
                continue
            try:
                new_name = "%s%s" % (prefix, node)
                mc.rename(node, new_name)
            except:
                pass


def unlock_normals():
    meshes = mc.ls(type="mesh")
    mc.select(meshes, r=1)
    unlock_normal.unlock_normal()


def convert_image(context):
    tex_dir = context.tex_dir
    if not os.path.isdir(tex_dir):
        return
    ext_list = [".tif", ".tiff", ".png", ".tga", ".jpg", ".jpeg", ".exr", ".psd", ".bmp"]
    for i in os.listdir(tex_dir):
        tex_name = "%s/%s" % (tex_dir, i)
        if not os.path.isfile(tex_name):
            continue
        ext = os.path.splitext(tex_name)[-1]
        if ext not in ext_list:
            continue
        prefix, suffix = os.path.split(tex_name)
        half_tex_name = "%s/half/%s" % (prefix, suffix)
        half_tex_dir = os.path.dirname(half_tex_name)
        if not os.path.isdir(half_tex_dir):
            os.makedirs(half_tex_dir)
        resize_image(tex_name, half_tex_name)


def main(file_name, local):
    logger = logging.getLogger("shd publish")
    if not local:
        open_file.open_file(file_name)
    # get paths
    context = pipeFile.PathDetails.parse_path(file_name)
    publish_path = context.publish_path
    publish.copy_image_and_video(context)
    logger.info("copy image and video done.")
    # import all reference
    publish.reference_opt()
    logger.info("Import all reference.")
    # unlock normals
    unlock_normals()
    # delete history and delete unused nodes
    delete_history.delete_history()
    delete_unused_nodes.delete_unused_nodes()
    # delete intermediate object
    delete_intermediate_object.delete_intermediate_object()
    logger.info("Delete intermediate_object done.")
    # remove namespace
    remove_namespace.remove_namespace()
    logger.info("Remove namespace done.")
    # rename mat node
    model_name = get_model_name.get_model_name()
    mc.select(model_name, r=1)
    rename_shd_mat_node(context)
    logger.info("Rename material name done.")
    # rename shape
    if not rename_pipeline_shape.rename_pipeline_shape():
        raise RuntimeError("Rename shape error.")
    logger.info("Rename shape done.")
    # export _MODEL to publish path
    delete_layer.delete_layer()
    export_selected.export_selected(publish_path)
    logger.info("Export to %s" % publish_path)
    # export material
    publish.export_material(context)
    logger.info("Export material done.")
    # export connection
    publish.export_connection(context)
    logger.info("Export connection done.")
    # convert image
    convert_image(context)
    logger.info("Convert image done.")
    # add to AD
    publish.add_mesh_to_ad(context)
    logger.info("Add to AD done.")
    if not local:
        quit_maya.quit_maya()
