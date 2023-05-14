from PyQt5.QtWidgets import QPushButton

class ColumnActionButton(QPushButton):

    def __init__(self, column, parent=None):
        super().__init__(parent)
        self.column = column 