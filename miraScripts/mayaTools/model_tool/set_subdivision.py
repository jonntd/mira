# -*- coding: utf-8 -*-
from functools import partial
from Qt.QtWidgets import *
from Qt.QtCore import *
import maya.cmds as mc


class Subdivision(QDialog):
    def __init__(self, parent=None):
        super(Subdivision, self).__init__(parent)
        self.setup_ui()
        self.set_signals()

    def setup_ui(self):
        self.setWindowTitle("Subdivision")
        self.setWindowFlags(Qt.Window)
        self.resize(300, 100)

        main_layout = QVBoxLayout(self)
        self.sub_on_btn = QPushButton("Subdivision On")
        self.sub_off_btn = QPushButton("Subdivision Off")

        separator_layout = QHBoxLayout()
        separator_layout.setContentsMargins(0, 10, 0, 10)
        separator_layout.setAlignment(Qt.AlignVCenter)
        frame = QFrame()
        frame.setFrameStyle(QFrame.HLine)
        frame.setStyleSheet('QFrame{color: #111111}')
        separator_layout.addWidget(frame)

        self.dis_on_btn = QPushButton("Displacement On")
        self.dis_off_btn = QPushButton("Displacement Off")

        main_layout.addWidget(self.sub_on_btn)
        main_layout.addWidget(self.sub_off_btn)
        main_layout.addLayout(separator_layout)
        main_layout.addWidget(self.dis_on_btn)
        main_layout.addWidget(self.dis_off_btn)

    def set_signals(self):
        self.sub_on_btn.clicked.connect(partial(self.set_attr, "rsEnableSubdivision", 1))
        self.sub_off_btn.clicked.connect(partial(self.set_attr, "rsEnableSubdivision", 0))
        self.dis_on_btn.clicked.connect(partial(self.set_attr, "rsEnableDisplacement", 1))
        self.dis_off_btn.clicked.connect(partial(self.set_attr, "rsEnableDisplacement", 0))

    def get_sel(self):
        return mc.ls(sl=1)

    def set_attr(self, attr, status):
        selected = self.get_sel()
        if not selected:
            return
        for sel in selected:
            mc.setAttr("%s.%s" % (sel, attr), status)


def main():
    from miraLibs.qtLibs import render_ui
    render_ui.render(Subdivision)


if __name__ == "__main__":
    main()
