from PyQt5.QtWidgets import QPushButton, QWidget, QSpinBox, QLabel, QScrollArea
from ui.PandasHistogram import PandasHistogram
from PyQt5.QtWidgets import QPushButton, QMainWindow
from PyQt5.QtWidgets import QVBoxLayout
from ui.IntervalPicker import IntervalPicker
from preprocessing.standarizer.Standarizer import Standarizer
from PyQt5.QtWidgets import QVBoxLayout
from ui.layout_cleaner import clean_layout
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QAbstractItemView

class IntervalPickerButton(QPushButton):
    def __init__(self, standarizer: Standarizer, column, columns, parent=None):
        super().__init__(parent)
        self.setText("Dostosuj przedziały")
        self.window = QMainWindow()
        self.window.setFixedWidth(500)
        self.window.setFixedHeight(500)
        self.clicked.connect(self.make_intervals)
        self.standarizer = standarizer
        self.column = column
        self.columns = columns
        self.label = QLabel("Zmień ilość wartości: ")
        self.values = QSpinBox()
        self.values.setValue(self.standarizer.getBoundary(self.column))
        self.values.valueChanged.connect(self.setBoundary)
        self.main_layout = QVBoxLayout()

    def getIntervals(self):
        return self.standarizer.getColumnIntervals(self.column)

    def setBoundary(self):
        self.standarizer.setBoundary(self.column, self.values.value())
        clean_layout(self.main_layout)
        self.make_intervals()

    def apply_intervals(self):
        columns = [x.text for x in self.column_selector.selectedItems()]
        intervals = self.picker.get_from_picker()

        for column in columns:
            self.standarizer.setIntervals(column, intervals)
        self.standarizer.setIntervals(self.column, intervals)

    def make_intervals(self):
        self.picker = IntervalPicker(self.standarizer.getIntervals()[self.column])

        self.selector_label = QLabel("Wybierz kolumny, do zaaplikowania tych samych ustawień")
        self.column_selector = QListWidget()
        self.column_selector.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.confirm_button = QPushButton("Zastosuj")
        self.confirm_button.clicked.connect(self.apply_intervals)

        for column in self.columns:
            item = QListWidgetItem(column)
            self.column_selector.addItem(item)

        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.values)
        self.picker.add_to_layout(self.main_layout)
        self.main_layout.addWidget(self.selector_label)
        self.main_layout.addWidget(self.column_selector)
        self.main_layout.addWidget(self.confirm_button)
        self.scroll = QScrollArea()
        self.widget = QWidget()

        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.widget.setLayout(self.main_layout)
        self.window.setCentralWidget(self.scroll)

        self.window.show()
