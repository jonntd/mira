from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
from Qt import __binding__
import maya.OpenMayaUI as mui
import get_engine


def get_maya_win(module="PySide"):
    """
    get a QMainWindow Object of maya main window
    :param module (optional): string "PySide"(default) or "PyQt4"
    :return main_window: QWidget or QMainWindow object
    """
    prt = mui.MQtUtil.mainWindow()
    if module == "PyQt":
        import sip
        from Qt.QtCore import *
        main_window = sip.wrapinstance(long(prt), QObject)
    elif module in ["PySide", "PyQt"]:
        if __binding__ in ["PySide", "PyQt4"]:
            import shiboken
        elif __binding__ in ["PySide2", "PyQt5"]:
            import shiboken2 as shiboken
        from Qt.QtWidgets import *
        main_window = shiboken.wrapInstance(long(prt), QWidget)
    elif module == "mayaUI":
        main_window = "MayaWindow"
    else:
        raise ValueError('param "module" must be "mayaUI" "PyQt4" or "PySide"')
    return main_window


def get_nuke_win():
    app = QApplication.instance()
    nuke_win = app.activeWindow()
    return nuke_win


def get_parent_win():
    parent_win = None
    engine = get_engine.get_engine()
    if engine == "maya":
        parent_win = get_maya_win("PySide")
    elif engine == "nuke":
        parent_win = get_nuke_win()
    else:
        # todo
        print "add method to how to get main window."
    return parent_win
