# # -*- coding: utf-8 -*-
import logging
import os
from Qt.QtWidgets import *
from Qt.QtCore import *
import maya.cmds as mc
import xgenm as xgen
from miraLibs.mayaLibs import get_namespace, export_abc
from miraLibs.pipeLibs import pipeFile, Project
from miraFramework.FrameLayout import FrameLayout
from miraLibs.pyLibs import start_file


def export_geometry_cache(directory, file_name, start, end, points):
    if not os.path.isdir(directory):
        os.makedirs(directory)
    mc.cacheFile(refresh=True, directory=directory, singleCache=0, format="OneFile", smr=1, spm=1, cacheFormat='mcc',
                 fileName=file_name, st=start, et=end, points=points)


def get_max_frame():
    end_frame = mc.playbackOptions(q=1, max=1)
    return int(end_frame)


def get_version():
    context = pipeFile.PathDetails.parse_path()
    version = "v%s" % context.version
    return version


def get_cache_dir():
    context = pipeFile.PathDetails.parse_path()
    project = context.project
    template = Project(project).template("fx_cache_work")
    cache_dir = template.format(project=project, sequence=context.sequence, shot=context.shot, step="Cfx")
    return cache_dir


def export_sculp():
    sculps = [t for t in mc.ls(type="transform") if t.endswith("_SCULP")]
    if not sculps:
        return
    max_frame = get_max_frame()
    root_cache_dir = get_cache_dir()
    version = get_version()
    for sculp in sculps:
        namespace = get_namespace.get_namespace(sculp)
        cache_dir = "%s/%s/%s/sculp" % (root_cache_dir, version, namespace)
        children = mc.listRelatives(sculp, c=1, type="transform")
        for t in children:
            no_namespace_name = t.split(":")[-1]
            shapes = mc.listRelatives(t, type="shape", ni=1)
            needed_shapes = list(set(shapes)-set(mc.ls(shapes, io=1)))
            if len(needed_shapes) != 1:
                logging.error("More than one shape under %s" % t)
                continue
            export_geometry_cache(cache_dir, no_namespace_name, 990, max_frame, needed_shapes[0])


def export_cloth(asset_name):
    sel = mc.ls(sl=1)
    if not sel:
        QMessageBox.warning(None, "Warming Tip", "Select something first.")
        return
    root_cache_dir = get_cache_dir()
    version = get_version()
    max_frame = get_max_frame()
    cache_file = "%s/%s/%s/cloth/cloth.abc" % (root_cache_dir, version, asset_name)
    cache_dir = os.path.dirname(cache_file)
    if not os.path.isdir(cache_dir):
        os.makedirs(cache_dir)
    export_abc.export_abc(990, max_frame, cache_file, sel, uv_write=False)


def export_hair_cache(description):
    sel = mc.ls(sl=1)
    if not sel:
        QMessageBox.warning(None, "Warming Tip", "Select something first.")
        return
    root_cache_dir = get_cache_dir()
    version = get_version()
    max_frame = get_max_frame()
    namespace = get_namespace.get_namespace(description)
    file_name = description.split(":")[-1]
    cache_file = "%s/%s/%s/hair/%s.abc" % (root_cache_dir, version, namespace, file_name)
    cache_dir = os.path.dirname(cache_file)
    if not os.path.isdir(cache_dir):
        os.makedirs(cache_dir)
    export_abc.export_abc(990, max_frame, cache_file, sel, uv_write=False)


def get_has_cloth_asset():
    if not mc.objExists("Char"):
        return
    characters = mc.listRelatives("Char", type="transform")
    if not characters:
        return
    characters = [get_namespace.get_namespace(char) for char in characters]
    return characters


def get_description():
    palettes = xgen.palettes()
    if not palettes:
        return
    descriptions = list()
    for palette in palettes:
        cell_desc = xgen.descriptions(palette)
        if cell_desc:
            descriptions.extend(cell_desc)
    return descriptions


class CfxExport(QDialog):
    def __init__(self, parent=None):
        super(CfxExport, self).__init__(parent)
        self.setup_ui()
        self.init()
        self.set_signals()

    def setup_ui(self):
        self.resize(420, 500)
        self.setWindowTitle("Cfx Export Cache.")
        self.setWindowFlags(Qt.Window)
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setContentsMargins(0, 0, 0, 0)

        sculp_frame_layout = FrameLayout("Export Sculp", False)
        sculp_layout = QHBoxLayout(sculp_frame_layout.frame)
        self.export_sculp_btn = QPushButton("Export Sculp")
        sculp_layout.addWidget(self.export_sculp_btn)
        main_layout.addLayout(sculp_frame_layout)

        cloth_frame_layout = FrameLayout("Export Cloth", False)
        cloth_layout = QVBoxLayout(cloth_frame_layout.frame)
        self.asset_name_list_widget = QListWidget()
        self.asset_name_list_widget.setSortingEnabled(True)
        self.asset_name_list_widget.setFocusPolicy(Qt.NoFocus)
        self.export_cloth_btn = QPushButton("Export Cloth")
        cloth_layout.addWidget(self.asset_name_list_widget)
        cloth_layout.addWidget(self.export_cloth_btn)
        main_layout.addLayout(cloth_frame_layout)

        hair_frame_layout = FrameLayout("Export Hair", False)
        hair_layout = QVBoxLayout(hair_frame_layout.frame)
        self.description_list_widget = QListWidget()
        self.description_list_widget.setSortingEnabled(True)
        self.description_list_widget.setFocusPolicy(Qt.NoFocus)
        self.export_hair_btn = QPushButton("Export Hair")
        hair_layout.addWidget(self.description_list_widget)
        hair_layout.addWidget(self.export_hair_btn)
        main_layout.addLayout(hair_frame_layout)

        self.launch_folder_btn = QPushButton("Launch Folder")
        self.launch_folder_btn.setStyleSheet("background: #006400;")
        main_layout.addWidget(self.launch_folder_btn)

    def init(self):
        # init char
        characters = get_has_cloth_asset()
        if characters:
            self.asset_name_list_widget.addItems(characters)
        # init description
        descriptions = get_description()
        if descriptions:
            self.description_list_widget.addItems(descriptions)

    def set_signals(self):
        self.export_sculp_btn.clicked.connect(export_sculp)
        self.export_cloth_btn.clicked.connect(self.export_cloth)
        self.export_hair_btn.clicked.connect(self.export_hair)
        self.launch_folder_btn.clicked.connect(self.launch_folder)

    def export_cloth(self):
        selected_items = self.asset_name_list_widget.selectedItems()
        if not selected_items:
            return
        asset_name = selected_items[0].text()
        export_cloth(asset_name)
        self.asset_name_list_widget.clearSelection()
        
    def export_hair(self):
        selected_items = self.description_list_widget.selectedItems()
        if not selected_items:
            return
        description = selected_items[0].text()
        export_hair_cache(description)
        self.description_list_widget.clearSelection()

    @staticmethod
    def launch_folder():
        cache_dir = get_cache_dir()
        if os.path.isdir(cache_dir):
            start_file.start_file(cache_dir)
        

def main():
    from miraLibs.qtLibs import render_ui
    render_ui.render(CfxExport)


if __name__ == "__main__":
    main()
