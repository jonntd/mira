# -*- coding: utf-8 -*-
import glob
import os
import maya.cmds as mc
from miraLibs.pipeLibs import pipeFile, Project
from miraLibs.mayaLibs import create_reference, create_group


def main():
    reference_cloth()
    group_cloth()


def reference_cloth():
    context = pipeFile.PathDetails.parse_path()
    project = context.project
    template = Project(project).template("fx_cache_publish")
    cache_dir = template.format(project=project, sequence=context.sequence, shot=context.shot, step="Cfx")
    if not os.path.isdir(cache_dir):
        print "No cloth cache dir exist"
        return
    cloth_cache_path = glob.glob("%s/*/cloth/cloth.abc" % cache_dir)
    if cloth_cache_path:
        for cache in cloth_cache_path:
            create_reference.create_reference(cache, "cloth")
    else:
        print "No cloth cache found."


def group_cloth():
    top_ = mc.ls(assemblies=1)
    clothes = [i for i in top_ if i.startswith("cloth:")]
    if clothes:
        create_group.create_group("Cloth")
        for cloth in clothes:
            create_group.create_group(cloth, "Cloth")


if __name__ == "__main__":
    main()
