import pandas as pd
from PyQt5.QtWidgets import QTableView
from PyQt5.QtCore import QAbstractTableModel
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from ui.DataframeTableModel import TableModel

class DataframeReader:

    def __init__(self, file_name):
        self.file_name = file_name

    def make_table(self):
        df = pd.read_csv(self.file_name)
        model = TableModel(df.head())

        table = QTableView()
        table.setModel(model)

        return table