import os
from functools import partial
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
from miraFramework.combo import combo, project_combo
from miraLibs.stLibs import St
from miraLibs.pipeLibs import Project
from miraLibs.pyLibs import start_file, copytree


class Label(QLabel):
    def __init__(self, name=None, parent=None):
        super(Label, self).__init__(parent)
        self.name = name
        self.setText(self.name)
        self.setFixedWidth(60)
        self.setAlignment(Qt.AlignRight)


class PublishGui(QDialog):
    def __init__(self, root_dir=None, parent=None):
        super(PublishGui, self).__init__(parent)
        self.root_dir = root_dir
        self.version_dir = None
        self.setup_ui()
        self.init()
        self.set_signals()

    def setup_ui(self):
        self.resize(500, 400)
        self.setWindowTitle("publish")
        main_layout = QVBoxLayout(self)

        path_layout = QHBoxLayout()
        self.path_le = QLineEdit()
        self.open_btn = QToolButton()
        icon = QIcon()
        icon.addPixmap(self.style().standardPixmap(QStyle.SP_DirOpenIcon))
        self.open_btn.setIcon(icon)
        path_layout.addWidget(self.path_le)
        path_layout.addWidget(self.open_btn)

        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("QListView::item:selected{background: #ff8c00};")
        btn_layout = QHBoxLayout()
        self.publish_btn = QPushButton("Publish")
        btn_layout.addStretch()
        btn_layout.addWidget(self.publish_btn)

        main_layout.addLayout(path_layout)
        main_layout.addWidget(self.list_widget)
        main_layout.addLayout(btn_layout)

    def set_signals(self):
        self.open_btn.clicked.connect(self.open_dir)
        self.list_widget.itemPressed.connect(self.set_path)
        self.publish_btn.clicked.connect(self.do_publish)

    def do_close(self):
        self.close()
        self.deleteLater()

    def open_dir(self):
        dir_ = self.path_le.text()
        if os.path.isdir(dir_):
            start_file.start_file(dir_)

    def init(self):
        self.path_le.setText(self.root_dir)
        if os.path.isdir(self.root_dir):
            version_dirs = os.listdir(self.root_dir)
            self.list_widget.addItems(version_dirs)

    def set_path(self, item):
        text = item.text()
        path = "%s/%s" % (self.root_dir, text)
        self.path_le.setText(path)

    def do_publish(self):
        self.version_dir = self.path_le.text()
        self.do_close()


class FxPublish(QDialog):
    def __init__(self, parent=None):
        super(FxPublish, self).__init__(parent)
        self.setWindowFlags(Qt.Window)
        self.setWindowTitle("[Cfx Vfx Lgt] publish ")
        self.resize(350, 200)
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setSpacing(10)

        entity_layout = QGridLayout()
        project_label = Label("Project")
        self.project_combo = project_combo.ProjectCombo()
        sequence_label = Label("Sequence")
        self.sequence_le = QLineEdit()
        shot_label = Label("Shot")
        self.shot_le = QLineEdit()
        step_label = Label("Step")
        self.step_combo = combo.CombBox()

        entity_layout.addWidget(project_label, 0, 0)
        entity_layout.addWidget(self.project_combo, 0, 1)
        entity_layout.addWidget(sequence_label, 1, 0)
        entity_layout.addWidget(self.sequence_le, 1, 1)
        entity_layout.addWidget(shot_label, 2, 0)
        entity_layout.addWidget(self.shot_le, 2, 1)
        entity_layout.addWidget(step_label, 3, 0)
        entity_layout.addWidget(self.step_combo, 3, 1)
        entity_layout.setSpacing(10)

        check_layout = QHBoxLayout()
        self.cache_check = QCheckBox("Cache")
        self.shot_check = QCheckBox("Render")
        check_layout.addWidget(self.cache_check)
        check_layout.addWidget(self.shot_check)
        self.btn_group = QButtonGroup(self)
        self.btn_group.addButton(self.cache_check)
        self.btn_group.addButton(self.shot_check)

        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(0)
        self.launch_workarea_btn = QPushButton("Launch Workarea")
        self.launch_publish_btn = QPushButton("Launch Publish")
        btn_layout.addWidget(self.launch_workarea_btn)
        btn_layout.addWidget(self.launch_publish_btn)

        self.change_status_check = QCheckBox("Change task status to \"Delivered\"")
        self.publish_btn = QPushButton("Publish")

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setRange(0, 10)
        self.progress_bar.hide()
        self.publish_btn.setMinimumHeight(30)
        main_layout.addLayout(entity_layout)
        main_layout.addLayout(check_layout)
        main_layout.addLayout(btn_layout)
        main_layout.addWidget(self.change_status_check)
        main_layout.addWidget(self.publish_btn)
        main_layout.addWidget(self.progress_bar)

        self.init()
        self.set_signals()

    @property
    def project(self):
        return self.project_combo.currentText()

    @property
    def sequence(self):
        return self.sequence_le.text()

    @property
    def shot(self):
        return self.shot_le.text()

    @property
    def step(self):
        return self.step_combo.currentText()

    @property
    def submit_type(self):
        checked_btn = self.btn_group.checkedButton()
        return checked_btn.text() if checked_btn else None

    def init(self):
        self.db = St.St(self.project)
        self.init_sequence()
        self.init_step()

    def set_signals(self):
        self.sequence_le.editingFinished.connect(self.init_shot)
        self.project_combo.currentIndexChanged.connect(self.on_project_changed)
        self.launch_workarea_btn.clicked.connect(partial(self.launch_dir, "work"))
        self.launch_publish_btn.clicked.connect(partial(self.launch_dir, "publish"))
        self.publish_btn.clicked.connect(self.do_publish)

    def on_project_changed(self):
        self.sequence_le.setText("")
        self.shot_le.setText("")
        self.init()
        self.task_le.setText("")

    def init_sequence(self):
        sequences = self.db.get_all_sequences()
        if not sequences:
            return
        sequences.sort()
        completer = QCompleter(sequences)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.sequence_le.setCompleter(completer)

    def init_shot(self):
        shots = self.db.get_all_shots(self.sequence)
        if not shots:
            return
        shots = [shot.get("code").split("_")[-1] for shot in shots]
        shots.sort()
        completer = QCompleter(shots)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.shot_le.setCompleter(completer)

    def init_step(self):
        shot_steps = ["Cfx", "CfxLay", "VfxLay", "Vfx", "LgtLay", "Lgt"]
        self.step_combo.addItems(shot_steps)
        self.step_combo.setCurrentIndex(self.step_combo.count()+1)

    def get_dir(self, step, work_type, submit_type=None):
        if step in ["LgtLay", "Lgt"]:
            if work_type == "work":
                template = Project(self.project).template("maya_shot_render")
            else:
                template = Project(self.project).template("maya_shot_renderPublish")
        else:
            if work_type == "work":
                if submit_type == "Cache":
                    template = Project(self.project).template("fx_cache_work")
                else:
                    template = Project(self.project).template("fx_render_work")
            else:
                if submit_type == "Cache":
                    template = Project(self.project).template("fx_cache_publish")
                else:
                    template = Project(self.project).template("fx_render_publish")
        return template.format(project=self.project, sequence=self.sequence, shot=self.shot, step=self.step)

    def launch_dir(self, work_type):
        dir_ = self.get_dir(self.step, work_type, self.submit_type)
        if os.path.isdir(dir_):
            start_file.start_file(dir_)

    def do_publish(self):
        dir_ = self.get_dir(self.step, "work", self.submit_type)
        publish_dir = self.get_dir(self.step, "publish", self.submit_type)
        pg = PublishGui(dir_, self)
        pg.exec_()
        version_dir = pg.version_dir
        if version_dir:
            self.progress_bar.show()
            self.progress_bar.setValue(3)
            try:
                copytree.copytree(version_dir, publish_dir)
                self.progress_bar.setValue(8)
            except:
                self.progress_bar.hide()
                QMessageBox.critical(self, "Error", "Copy to publish failed.")
            else:
                if self.change_status_check.isChecked():
                    current_task = self.db.get_current_task("Shot", self.sequence, self.shot, self.step, self.step)
                    if current_task:
                        self.db.update_task_status(current_task, "Delivered")
                self.progress_bar.setValue(10)
                self.progress_bar.hide()
                QMessageBox.information(self, "Warming Tip", "Publish Successful.")


def main():
    from miraLibs.qtLibs import render_ui
    render_ui.render(FxPublish)


if __name__ == "__main__":
    main()
