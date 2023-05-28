from PyQt5.QtWidgets import *

class ColumnCheckbox(QCheckBox):

    def __init__(self, column, parent=None):
        super().__init__(parent)
        self.column = column