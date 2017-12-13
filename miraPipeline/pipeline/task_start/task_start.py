# -*- coding: utf-8 -*-
import os
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
from miraLibs.pipeLibs.get_task_name import get_task_name
from miraFramework.task_common_form import CommonForm
from miraLibs.pyLibs import Path, join_path
from miraLibs.pipeLibs import pipeFile, Step
from miraLibs.deadlineLibs import submit_python
from miraLibs.qtLibs import render_ui


class TaskStart(QDialog):
    def __init__(self, parent=None):
        super(TaskStart, self).__init__(parent)
        self.setup_ui()
        self.set_style()
        self.set_signals()

    def setup_ui(self):
        self.setWindowFlags(Qt.Window)
        self.setWindowTitle("Task Start")
        self.resize(800, 600)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.common_widget = CommonForm()
        bottom_layout = QHBoxLayout()
        self.path_le = QLineEdit()
        self.path_btn = QToolButton()
        icon = QIcon()
        icon.addPixmap(self.style().standardPixmap(QStyle.SP_DirOpenIcon))
        self.path_btn.setIcon(icon)
        bottom_layout.addWidget(self.path_le)
        bottom_layout.addWidget(self.path_btn)

        btn_layout = QHBoxLayout()
        self.start_btn = QPushButton("Start")
        btn_layout.addStretch()
        btn_layout.addWidget(self.start_btn)

        main_layout.addWidget(self.common_widget)
        main_layout.addLayout(bottom_layout)
        main_layout.addLayout(btn_layout)

    def set_style(self):
        qss_path = join_path.join_path2(os.path.dirname(__file__), "style.qss")
        self.setStyle(QStyleFactory.create('plastique'))
        self.setStyleSheet(open(qss_path, 'r').read())

    def set_signals(self):
        self.common_widget.fourth_widget.list_view.clicked.connect(self.show_path)
        self.path_btn.clicked.connect(self.open_dir)
        self.start_btn.clicked.connect(self.do_start)

    @property
    def work_file(self):
        return self.path_le.text()

    @property
    def task_info(self):
        return self.common_widget.task_info

    def can_publish(self, project, entity_type, asset_type_or_sequence, asset_or_shot, step, task):
        file_path = pipeFile.get_task_work_file(project, entity_type, asset_type_or_sequence,
                                                asset_or_shot, step, task, "000")
        self.path_le.setText(file_path)
        self.start_btn.setEnabled(True)

    def show_path(self):
        project = self.common_widget.project
        entity_type = self.common_widget.entity_type
        asset_type_or_sequence = self.common_widget.asset_type_or_sequence
        asset_or_shot = self.common_widget.asset_or_shot
        step = self.common_widget.step
        task = self.common_widget.task
        if not all((asset_type_or_sequence, asset_or_shot, step, task)):
            return
        up_steps = Step(project, step).up_step
        if up_steps:
            up_step_published = True
            for up_step in up_steps:
                publish_file = pipeFile.get_task_publish_file(project, entity_type, asset_type_or_sequence,
                                                              asset_or_shot, up_step, up_step, "")
                if not publish_file or not os.path.isfile(publish_file):
                    up_step_published = False
                    break
            if up_step_published:
                self.can_publish(project, entity_type, asset_type_or_sequence, asset_or_shot, step, task)
            else:
                self.path_le.setText(u"上一环节没有publish")
                self.start_btn.setDisabled(True)
        else:
            self.can_publish(project, entity_type, asset_type_or_sequence, asset_or_shot, step, task)

    def open_dir(self):
        path = self.path_le.text()
        if path:
            p = Path.Path(path)
            dir_name = Path.Path(p.dirname())
            dir_name.startfile()

    def do_start(self):
        if not self.work_file:
            return
        start_script_path = join_path.join_path2(__file__, "..", "start.py")
        obj = pipeFile.PathDetails.parse_path(self.work_file)
        task_name = get_task_name(obj)
        deadline_job_name = "start_%s" % task_name
        # work_file, change_task
        argv = self.work_file
        white_list = 'pipemanager'
        submit_python.submit_python(start_script_path, argv, white_list, deadline_job_name)
        QMessageBox.information(self, "Warming Tip", "%s submit done." % task_name)


def main():
    render_ui.render(TaskStart)


if __name__ == "__main__":
    main()
