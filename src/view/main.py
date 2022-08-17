from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.QtCore import pyqtSlot
from view.main_ui import Ui_MainWindow


class MainView(QMainWindow):
    def __init__(self, model, main_controller):
        super().__init__()

        self._model = model
        self._main_controller = main_controller
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        self._ui.addButton.clicked.connect(self.loadFiles)
        self._ui.removeButton.clicked.connect(self.removeFile)
        self._ui.calculateButton.clicked.connect(
            lambda: self._main_controller.calculate()
        )

        self._model.files_changed.connect(self.on_list_changed)
        self._model.df_changed.connect(self.on_df_changed)

    def loadFiles(self):
        filter = "XML (*.xml)"
        file_name = QFileDialog()
        file_name.setFileMode(QFileDialog.ExistingFiles)
        names = file_name.getOpenFileNames(self, "Open files", "C\\Desktop", filter)
        self._main_controller.add_files(names)

    def removeFile(self):
        self._main_controller.delete_file(self._ui.listView.currentRow())

    @pyqtSlot(list)
    def on_list_changed(self, value):
        self._ui.listView.clear()
        self._ui.listView.addItems(value)

    @pyqtSlot(object)
    def on_df_changed(self, value):
        self._ui.tableWidget.setModel(value)