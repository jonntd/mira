# -*- coding: utf-8 -*-
from Qt.QtWidgets import *
from Qt.QtCore import *
from miraLibs.pipeLibs.pipeMaya.lgt import replace_env, import_cloth, import_hair_cache
reload(import_hair_cache)


class LgtInit(QDialog):
    def __init__(self, parent=None):
        super(LgtInit, self).__init__(parent)
        self.setup_ui()
        self.set_signals()

    def setup_ui(self):
        self.setWindowTitle("Lgt initialize")
        self.resize(250, 150)
        self.setWindowFlags(Qt.Window)
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop)
        self.replace_env_btn = QPushButton(u"替换场景")
        self.import_cloth_btn = QPushButton(u"导入布料")
        label = QLabel()
        label.setText(u"<font color=#ff9c00 face=Arial><b>先导入毛发，再继续下面的操作</b></font>")
        self.import_hair_cache_btn = QPushButton(u"导入毛发缓存")
        main_layout.addWidget(self.replace_env_btn)
        main_layout.addWidget(self.import_cloth_btn)
        main_layout.addWidget(label)
        main_layout.addWidget(self.import_hair_cache_btn)
        
    def set_signals(self):
        self.replace_env_btn.clicked.connect(replace_env.main)
        self.import_cloth_btn.clicked.connect(import_cloth.main)
        self.import_hair_cache_btn.clicked.connect(import_hair_cache.main)


def main():
    from miraLibs.qtLibs import render_ui
    render_ui.render(LgtInit)

