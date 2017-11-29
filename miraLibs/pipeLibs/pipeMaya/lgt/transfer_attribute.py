# -*- coding: utf-8 -*-
import maya.cmds as mc


attrs = ["rsEnableSubdivision", "rsSubdivisionRule", "rsScreenSpaceAdaptive", "rsDoSmoothSubdivision",\
         "rsMinTessellationLength", "rsMaxTessellationSubdivs", "rsOutOfFrustumTessellationFactor",
         "rsEnableDisplacement", "rsMaxDisplacement", "rsDisplacementScale", "rsAutoBumpMap"]


def transfer_attribute():
    deformed_meshes = mc.ls("*Deformed", long=1)
    if not deformed_meshes:
        return
    for mesh in deformed_meshes:
        transform = mc.listRelatives(mesh, p=1, fullPath=1)[0]
        shapes = mc.listRelatives(transform, c=1, fullPath=1)
        io_shape = mc.ls(shapes, io=1, long=1)
        if not io_shape:
            continue
        for attr in attrs:
            mc.setAttr("%s.%s" % (mesh, attr), mc.getAttr("%s.%s" % (io_shape[0], attr)))
