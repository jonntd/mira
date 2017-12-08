# -*- coding: utf-8 -*-
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *


class FrameLayout(QVBoxLayout):
    def __init__(self, button_text=None, collapse_status=None, parent=None):
        super(FrameLayout, self).__init__(parent)
        self.button_text = button_text
        self.collapse_status = collapse_status
        self.parent = parent

        self.setSpacing(0)

        self.tool_btn = QToolButton()
        self.tool_btn.setText(self.button_text)
        self.tool_btn.setIconSize(QSize(6, 6))
        self.tool_btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.tool_btn.setStyleSheet("QToolButton {background: transparent}")

        self.frame = QFrame()
        self.frame.setFrameStyle(QFrame.Panel | QFrame.Sunken)

        self.addWidget(self.tool_btn)
        self.addWidget(self.frame)
        self.init_settings()
        self.set_signals()

    def init_settings(self):
        if self.collapse_status:
            self.tool_btn.setArrowType(Qt.RightArrow)
            self.frame.setHidden(True)
        else:
            self.tool_btn.setArrowType(Qt.DownArrow)
            self.frame.setHidden(False)

    def set_signals(self):
        self.tool_btn.clicked.connect(self.change_collapse)

    def change_collapse(self):
        self.collapse_status = not self.collapse_status
        self.init_settings()


if __name__ == "__main__":
    pass
