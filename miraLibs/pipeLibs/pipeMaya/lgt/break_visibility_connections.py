# -*- coding: utf-8 -*-
import maya.cmds as mc


def break_visibility_connections():
    exo_nodes = mc.ls(type="ExocortexAlembicXform")
    if not exo_nodes:
        return
    for exo_node in exo_nodes:
        src = "%s.outVisibility" % exo_node
        dst_attrs = mc.connectionInfo(src, destinationFromSource=1)
        if not dst_attrs:
            continue
        mc.disconnectAttr(src, dst_attrs[0])
