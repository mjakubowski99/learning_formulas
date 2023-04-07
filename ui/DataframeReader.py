import pandas as pd
from PyQt5.QtWidgets import QTableView, QPushButton
from PyQt5.QtCore import QAbstractTableModel
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from ui.DataframeTableModel import TableModel

class DataframeReader:

    def __init__(self, file_name):
        self.file_name = file_name
        self.model = None

    def make_table(self):
        df = pd.read_csv(self.file_name)
        self.model = TableModel(df)

        table = QTableView()
        table.setModel(self.model)

        return table
    
    def add_pagination_to_layout(self, layout):
        next_button = QPushButton('Next')
        next_button.clicked.connect(self.model.nextPage)

        prev_button = QPushButton('Previous')
        prev_button.clicked.connect(self.model.previousPage)
        
        layout.addWidget(next_button)
        layout.addWidget(prev_button)