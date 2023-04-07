import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSlider, QLineEdit, QLabel
from PyQt5.QtWidgets import QFileDialog
from ui.output_reader import ProcessOutputReader, MyConsole
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from ui.LabeledInput import LabeledInput
from ui.DataframeReader import DataframeReader

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 1270, 720)

        self.widget = QWidget()
        self.layout = QVBoxLayout(self.widget)
        self._process_reader = ProcessOutputReader()
        self.console = MyConsole()
        self.input_layout = QHBoxLayout()

        self.cycles_input = LabeledInput("Ilość cykli:", "20").add_to_layout(self.input_layout)
        self.formulas_input = LabeledInput("Ilość formuł: ", "100").add_to_layout(self.input_layout)
        self.clauses_input = LabeledInput("Ilość klauzul: ", "5").add_to_layout(self.input_layout)
        self.literals_input = LabeledInput("Ilość literałów: ", "3").add_to_layout(self.input_layout)


        self.selected_file = None 


        self.button_layout = QHBoxLayout()

        self.file_dialog = QFileDialog()
        self.file_dialog.setFileMode(QFileDialog.AnyFile)

        self.start_button = QPushButton("Rozpocznij uczenie")
        self.start_button.resize(50,50)
        self.start_button.clicked.connect(self.start_formula_learning)

        self.stop_button = QPushButton("Zakończ proces uczenia")
        self.stop_button.resize(50,50)
        self.stop_button.clicked.connect(self.stop_formula_learning)

        self.load_file = QPushButton("Załaduj plik")
        self.load_file.clicked.connect(self.open_file_dialog)

        self.button_layout.addWidget(self.start_button)
        self.button_layout.addWidget(self.stop_button)
        self.button_layout.addWidget(self.load_file)

        self.layout.addLayout(self.input_layout)
        self.layout.addLayout(self.button_layout)
        self.layout.addWidget(self.console)
        
        # set the central widget of the main window to the new widget
        self.setCentralWidget(self.widget)

    def open_file_dialog(self):
        self.file_dialog = QFileDialog()
        self.file_dialog.setFileMode(QFileDialog.AnyFile)
        self.file_dialog.exec_()
        self.selected_file = self.file_dialog.selectedFiles()[0]
        self.reader = DataframeReader(self.selected_file)
        self.layout.addWidget(self.reader.make_table())
        self.reader.add_pagination_to_layout(self.layout)
    
    def stop_formula_learning(self):
        self._process_reader.kill()
        self.console.append_output("Process stopped...")

    def start_formula_learning(self):
        self.console.clear_output()
        self._process_reader.produce_output.connect(self.console.append_output)
        self._process_reader.start('./core/build/learning_formulas', [
            'core/train.txt',
            'core/test.txt',
            self.cycles_input.get_value(),
            self.formulas_input.get_value(),
            self.clauses_input.get_value(),
            self.literals_input.get_value(),
            "result/"
        ])

    @pyqtSlot()
    def _delete_process_reader(self):
        self.layout.removeWidget(self.console)
        self.console.setParent(None)


app = QApplication(sys.argv)
main_window = MainWindow()

#main_window.start_formula_learning()
main_window.show()
sys.exit(app.exec_())