# -*- coding: utf-8 -*-
import os
import xgenm as xgen
import xgenm.xgGlobal as xgg
from miraLibs.pipeLibs import pipeFile, Project


def main():
    import_xgen_cache()


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
        for description in descriptions:
            cache_dir = get_cache_dir()
            cache_file_name = "%s/%s/hair/%s.abc" % (cache_dir, asset_name, description)
            if not os.path.isfile(cache_file_name):
                continue
            xgen.setAttr("useCache", "true", palette, description, "SplinePrimitive")
            xgen.setAttr("liveMode", "false", palette, description, "SplinePrimitive")
            xgen.setAttr("cacheFileName", cache_file_name, palette, description, "SplinePrimitive")

    de = xgg.DescriptionEditor
    de.refresh("Full")
