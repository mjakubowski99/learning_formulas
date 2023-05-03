from PyQt5.QtCore import QAbstractTableModel, QVariant
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
import pandas as pd

class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data.head(100)
        self._data = data.iloc[:, :20]

    def update_data(self, data):
        self._data = data.head(100)
        self._data = data.iloc[:, :20]
        self.layoutChanged.emit()

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return str(self._data.iloc[index.row(), index.column()])
        elif role == Qt.BackgroundRole:
            if pd.isnull(self._data.iloc[index.row(), index.column()]):
                return QColor(Qt.red)
        return QVariant()

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return str(self._data.columns[section])
        elif role == Qt.DisplayRole and orientation == Qt.Vertical:
            return str(self._data.index[section])
        return QVariant()
