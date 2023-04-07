from PyQt5.QtCore import QAbstractTableModel
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
import pandas as pd

class TableModel(QAbstractTableModel):
    def __init__(self, data, rows_per_page=10):
        super().__init__()
        self._data = data
        self._rows_per_page = rows_per_page
        self._current_page = 0

    @QtCore.pyqtSlot(int, QtCore.Qt.Orientation, result=str)
    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self._data.columns[section]
            else:
                return str(self._data.index[section])
        return QtCore.QVariant()

    def rowCount(self, parent):
        start = self._current_page * self._rows_per_page
        end = min(start + self._rows_per_page, len(self._data))
        return end - start

    def columnCount(self, parent):
        return len(self._data.columns)

    def data(self, index, role):
        if role == Qt.DisplayRole:
            start = self._current_page * self._rows_per_page
            row = start + index.row()
            if row < len(self._data):
                return str(self._data.iloc[row, index.column()])

    def nextPage(self):
        if self._current_page < (len(self._data) // self._rows_per_page):
            self._current_page += 1
            self.layoutChanged.emit()

    def previousPage(self):
        if self._current_page > 0:
            self._current_page -= 1
            self.layoutChanged.emit()