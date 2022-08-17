from PyQt5.QtCore import QObject, pyqtSignal

from model.dataframe_model import PandasModel


class Model(QObject):

    files_changed = pyqtSignal(list)
    df_changed = pyqtSignal(object)

    @property
    def files(self):
        return self._files

    def add_files(self, value):
        self._files.extend(value)
        self.files_changed.emit(self._files)

    def delete_file(self, value):
        del self._files[value]
        self.files_changed.emit(self._files)

    def add_dataframe(self, value):
        self._df = PandasModel(value)
        self.df_changed.emit(self._df)

    def __init__(self):
        super().__init__()
        self._files = []
        self._df = object
