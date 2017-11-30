# -*- coding: utf-8 -*-
import os
import maya.cmds as mc
import pymel.core as pm
import xgenm as xgen
import xgenm.xgGlobal as xgg
from miraLibs.pipeLibs import pipeFile, Project


def main():
    import_xgen_cache()
    import_geo_cache()


def get_cache_dir():
    context = pipeFile.PathDetails.parse_path()
    project = context.project
    template = Project(project).template("fx_cache_dir")
    cache_dir = template.format(project=project, sequence=context.sequence, shot=context.shot, step="Cfx")
    return cache_dir


def import_xgen_cache():
    palettes = xgen.palettes()
    if not palettes:
        return
    for palette in palettes:
        asset_name = palette.split("_")[0]
        descriptions = xgen.descriptions(palette)
        if not descriptions:
            continue
        cache_dir = get_cache_dir()
        for description in descriptions:
            cache_file_name = "%s/%s/hair/%s.abc" % (cache_dir, asset_name, description)
            if not os.path.isfile(cache_file_name):
                continue
            xgen.setAttr("useCache", "true", palette, description, "SplinePrimitive")
            xgen.setAttr("liveMode", "false", palette, description, "SplinePrimitive")
            xgen.setAttr("cacheFileName", cache_file_name, palette, description, "SplinePrimitive")

    de = xgg.DescriptionEditor
    de.refresh("Full")


def import_geo_cache():
    sculps = [transform for transform in mc.ls(type="transform") if transform.endswith("_SCULP")]
    if not sculps:
        return
    cache_dir = get_cache_dir()
    for sculp in sculps:
        asset_name = sculp.split("_")[1]
        geos = mc.listRelatives(sculp, c=1, fullPath=1)
        if not geos:
            continue
        for geo in geos:
            geo_short_name = geo.split("|")[-1]
            xml_path = "%s/%s/sculp/%s.xml" % (cache_dir, asset_name, geo_short_name)
            xml_path = xml_path.replace("\\", "/")
            data_path = "%s/%s/sculp/%s.mcx" % (cache_dir, asset_name, geo_short_name)
            data_path = data_path.replace("\\", "/")
            if not all((os.path.isfile(xml_path), os.path.isfile(data_path))):
                continue
            pm.mel.doImportCacheFile(xml_path, data_path, [geo], list())
            print "Attach cache to %s done" % geo
