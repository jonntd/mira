# -*- coding: utf-8 -*-
import os
import glob
import maya.cmds as mc
from miraLibs.pipeLibs import pipeFile, Project
from miraLibs.mayaLibs import create_reference, create_group


def main():
    reference_vfx()
    group_vfx()


def reference_vfx():
    context = pipeFile.PathDetails.parse_path()
    project = context.project
    template = Project(project).template("fx_cache_publish")
    cache_dir = template.format(project=project, sequence=context.sequence, shot=context.shot, step="Vfx")
    if not os.path.isdir(cache_dir):
        print "No cloth cache dir exist"
        return
    vfx_cache_path = glob.glob("%s/*.abc" % cache_dir)
    if vfx_cache_path:
        for cache in vfx_cache_path:
            create_reference.create_reference(cache, "vfx")
    else:
        print "No Vfx cache found."


def group_vfx():
    top_ = mc.ls(assemblies=1)
    vfxes = [i for i in top_ if i.startswith("vfx:")]
    if vfxes:
        create_group.create_group("Vfx")
        for vfx in vfxes:
            create_group.create_group(vfx, "Vfx")
