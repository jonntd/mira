# -*- coding: utf-8 -*-
from PySide import QtGui, QtCore
import miraCore
from miraFramework.Filter import ButtonLineEdit
from miraLibs.pyLibs import join_path
from miraLibs.pipeLibs import pipeMira, get_current_project
from miraLibs.sgLibs import Sg


ENGINELIST = ["maya", "nuke", "houdini"]


class ListModel(QtCore.QAbstractListModel):
    def __init__(self, model_data=[], parent=None):
        super(ListModel, self).__init__(parent)
        self.__model_data = model_data
        self.__model_data.sort()

    @property
    def model_data(self):
        return self.__model_data

    @model_data.setter
    def model_data(self, value):
        self.__model_data = value

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.__model_data)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            return self.__model_data[row]

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def insertRows(self, position, count, value, parent=QtCore.QModelIndex()):
        self.beginInsertRows(parent, position, position+count-1)
        for i in range(count):
            self.__model_data.insert(position, value)
        self.__model_data.sort()
        self.endInsertRows()
        return True

    def removeRows(self, position, count, parent=QtCore.QModelIndex()):
        self.beginRemoveRows(parent, position, position+count-1)
        for i in range(count):
            value = self.__model_data[position]
            self.__model_data.remove(value)
        self.endRemoveRows()
        return True


class ListView(QtGui.QListView):
    def __init__(self, parent=None):
        super(ListView, self).__init__(parent)
        self.menu = QtGui.QMenu()
        self.remove_action = QtGui.QAction("remove", self)
        self.setSelectionBehavior(QtGui.QListView.SelectRows)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setStyleSheet("QListView::item:selected{background: #ff8c00;}")

    def remove_item(self):
        model = self.model()
        if isinstance(model, QtGui.QSortFilterProxyModel):
            model = model.sourceModel()
        selected_indexes = self.selectedIndexes()
        if not selected_indexes:
            return
        count = 0
        selected_indexes = sorted(selected_indexes, key=lambda index: index.row())
        for i in selected_indexes:
            model.removeRows(i.row()-count, 1)
            count += 1

    def clear(self):
        model = self.model()
        if isinstance(model, QtGui.QSortFilterProxyModel):
            model = model.sourceModel()
        model.model_data = list()
        self.setModel(model)

    def get_items_data(self):
        items_data = list()
        model = self.model()
        if isinstance(model, QtGui.QSortFilterProxyModel):
            model = model.sourceModel()
        for i in xrange(model.rowCount(self)):
            model_index = model.index(i, 0)
            data = model_index.data()
            # data = self.list_model.data(model_index, QtCore.Qt.DisplayRole)
            items_data.append(str(data))
        return items_data

    def get_selected(self):
        selected = list()
        proxy_model = self.model()
        selected_indexes = self.selectedIndexes()
        if not selected_indexes:
            return
        selected_rows = list(set([proxy_model.mapToSource(i).row() for i in selected_indexes]))
        for row in selected_rows:
            value_index = proxy_model.sourceModel().index(row, 0)
            selected.append(value_index.data())
        return selected


class CommonWidget(QtGui.QWidget):
    add_signal = QtCore.Signal(basestring)

    def __init__(self, parent=None):
        super(CommonWidget, self).__init__(parent)
        self.resize(150, 180)
        self.model_data = list()
        self.group_name = None

        main_layout = QtGui.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.group_box = QtGui.QGroupBox()
        main_layout.addWidget(self.group_box)
        group_layout = QtGui.QVBoxLayout()

        horizon_layout = QtGui.QHBoxLayout()
        horizon_layout.setSpacing(0)
        icon_dir = miraCore.get_icons_dir()
        icon_path = join_path.join_path2(icon_dir, "search.png")
        self.filter_le = ButtonLineEdit(icon_path)
        horizon_layout.addWidget(self.filter_le)
        self.list_view = ListView()
        group_layout.addLayout(horizon_layout)
        group_layout.addWidget(self.list_view)
        self.group_box.setLayout(group_layout)
        self.set_model()
        # self.set_signals()

    def set_model(self):
        self.list_model = ListModel(self.model_data)
        self.proxy_model = QtGui.QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.list_model)
        self.proxy_model.setDynamicSortFilter(True)
        self.proxy_model.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.proxy_model.setSortCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.list_view.setModel(self.proxy_model)
        self.filter_le.textChanged.connect(self.proxy_model.setFilterRegExp)

    def set_signals(self):
        self.add_btn.clicked.connect(self.add)

    def set_group_name(self, value):
        self.group_box.setTitle(value)

    def set_model_data(self, value):
        if not value:
            return
        self.model_data = value
        self.set_model()

    def set_enable(self, value):
        if not value:
            self.filter_le.setEnabled(False)
            self.add_btn.setEnabled(False)
            self.list_view.setEnabled(False)
            self.list_view.clear()
        else:
            self.filter_le.setEnabled(True)
            self.add_btn.setEnabled(True)
            self.list_view.setEnabled(True)


class CommonForm(QtGui.QWidget):
    def __init__(self, parent=None):
        super(CommonForm, self).__init__(parent)
        self.__asset_types = pipeMira.get_asset_type()
        self.setup_ui()
        self.init()
        self.set_signals()
        self.sg = Sg.Sg(self.project)

    def setup_ui(self):
        main_layout = QtGui.QVBoxLayout(self)
        main_layout.setContentsMargins(3, 3, 3, 3)

        project_layout = QtGui.QHBoxLayout()
        project_label = QtGui.QLabel("Project")
        project_label.setFixedWidth(70)
        self.project_cbox = QtGui.QComboBox()
        project_layout.addWidget(project_label)
        project_layout.addWidget(self.project_cbox)

        entity_type_layout = QtGui.QHBoxLayout()
        style_label = QtGui.QLabel("Asset/Shot")
        style_label.setFixedWidth(70)
        self.entity_btn_grp = QtGui.QButtonGroup()
        self.asset_check = QtGui.QCheckBox("Asset")
        self.shot_check = QtGui.QCheckBox("Shot")
        self.entity_btn_grp.addButton(self.asset_check)
        self.entity_btn_grp.addButton(self.shot_check)
        entity_type_layout.addWidget(style_label)
        entity_type_layout.addWidget(self.asset_check)
        entity_type_layout.addWidget(self.shot_check)
        entity_type_layout.addStretch()

        engine_layout = QtGui.QHBoxLayout()
        engine_label = QtGui.QLabel("Engine")
        engine_label.setFixedWidth(70)
        engine_layout.addWidget(engine_label)
        self.engine_btn_grp = QtGui.QButtonGroup()
        for engine in ENGINELIST:
            self.engine_check_box = QtGui.QCheckBox(engine)
            if engine == "maya":
                self.engine_check_box.setChecked(True)
            self.engine_btn_grp.addButton(self.engine_check_box)
            engine_layout.addWidget(self.engine_check_box)
        engine_layout.addStretch()

        list_layout = QtGui.QHBoxLayout()
        list_layout.setContentsMargins(0, 3, 0, 3)
        self.first_widget = CommonWidget()
        self.second_widget = CommonWidget()
        self.third_widget = CommonWidget()
        self.third_widget.set_group_name("Step")
        self.fourth_widget = CommonWidget()
        self.fourth_widget.set_group_name("Task")
        list_layout.addWidget(self.first_widget)
        list_layout.addWidget(self.second_widget)
        list_layout.addWidget(self.third_widget)
        list_layout.addWidget(self.fourth_widget)

        separator_layout = QtGui.QHBoxLayout()
        separator_layout.setContentsMargins(0, 10, 0, 0)
        separator_layout.setAlignment(QtCore.Qt.AlignBottom)
        frame = QtGui.QFrame()
        frame.setFrameStyle(QtGui.QFrame.HLine)
        frame.setStyleSheet('QFrame{color: #111111; width: 10px}')
        separator_layout.addWidget(frame)

        main_layout.addLayout(project_layout)
        main_layout.addLayout(entity_type_layout)
        main_layout.addLayout(engine_layout)
        main_layout.addLayout(list_layout)
        main_layout.addLayout(separator_layout)

    @property
    def project(self):
        return self.project_cbox.currentText()

    @property
    def primary(self):
        return pipeMira.get_primary_dir(self.project)

    @property
    def mayabatch(self):
        return pipeMira.get_mayabatch_path(self.project)

    @property
    def engine(self):
        return self.engine_btn_grp.checkedButton().text()

    def init(self):
        projects = pipeMira.get_projects()
        self.project_cbox.addItems(projects)
        current_project = get_current_project.get_current_project()
        self.project_cbox.setCurrentIndex(self.project_cbox.findText(current_project))

    def set_signals(self):
        self.project_cbox.currentIndexChanged[str].connect(self.on_project_changed)
        self.entity_btn_grp.buttonClicked.connect(self.init_grp)
        self.first_widget.list_view.clicked.connect(self.show_asset_or_shot)
        self.second_widget.list_view.clicked.connect(self.show_step)
        self.third_widget.list_view.clicked.connect(self.show_task)

    def on_project_changed(self, project):
        self.sg = Sg.Sg(project)

    def init_grp(self):
        checked_btn_text = self.entity_btn_grp.checkedButton().text()
        for widget in [self.first_widget, self.second_widget, self.third_widget, self.fourth_widget]:
            widget.list_view.clear()
        if checked_btn_text == "Asset":
            # set group name
            self.first_widget.set_group_name("Asset Type")
            self.second_widget.set_group_name("Asset")
            self.second_widget.list_view.clear()
            # init list view
            self.first_widget.set_model_data(self.__asset_types)
        else:
            self.first_widget.set_group_name("Sequence")
            self.second_widget.set_group_name("Shot")
            self.second_widget.list_view.clear()
            # init list view
            sequences = self.sg.get_sequence()
            self.first_widget.set_model_data(sequences)

    def show_asset_or_shot(self, index):
        for widget in [self.second_widget, self.third_widget, self.fourth_widget]:
            widget.list_view.clear()
        selected = index.data()
        checked = self.entity_btn_grp.checkedButton().text()
        if checked == "Asset":
            assets = self.sg.get_all_assets(selected)
            asset_names = [asset["code"] for asset in assets]
            self.second_widget.set_model_data(asset_names)
        elif checked == "Shot":
            shots = self.sg.get_all_shots_by_sequence(selected)
            shot_names = [shot["name"] for shot in shots]
            self.second_widget.set_model_data(shot_names)

    def show_step(self, index):
        for widget in [self.third_widget, self.fourth_widget]:
            widget.list_view.clear()
        entity_type = self.entity_btn_grp.checkedButton().text()
        asset_or_shot = index.data()
        asset_type_or_sequence = self.first_widget.list_view.get_selected()
        if not asset_type_or_sequence:
            return
        steps = self.sg.get_step(entity_type, asset_type_or_sequence, asset_or_shot)
        step_names = [step["short_name"] for step in steps]
        self.third_widget.set_model_data(step_names)

    def show_task(self, index):
        self.fourth_widget.list_view.clear()
        entity_type = self.entity_btn_grp.checkedButton().text()
        asset_type_or_sequence = self.first_widget.list_view.get_selected()
        asset_or_shot = self.second_widget.list_view.get_selected()
        step = index.data()
        if not all((asset_type_or_sequence, asset_or_shot)):
            return
        tasks = self.sg.get_task(entity_type, asset_type_or_sequence, asset_or_shot, step)
        if not tasks:
            return
        task_names = [task["content"] for task in tasks]
        self.fourth_widget.set_model_data(task_names)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    cf = CommonForm()
    cf.show()
    app.exec_()