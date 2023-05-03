from PyQt5.QtWidgets import QPushButton
from ui.PandasHistogram import PandasHistogram
from PyQt5.QtWidgets import QPushButton, QMainWindow
from PyQt5.QtWidgets import QVBoxLayout

class ColumnButton(QPushButton):
    def __init__(self, df, column, text, parent=None):
        super().__init__(parent)
        self.df = df 
        self.column = column
        self.setText(text)
        self.window = QMainWindow()
        self.window.setWindowTitle(self.column)
        self.clicked.connect(self.make_hist)

    def make_hist(self):
        drawer = PandasHistogram()

        histogram = drawer.hist(self.df, self.column)
        histogram.setFixedWidth(400)

        self.window.setCentralWidget(histogram)

        self.window.show()
