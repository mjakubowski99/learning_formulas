import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QSlider, QLineEdit, QLabel
from PyQt5.QtWidgets import QFileDialog
from ui.output_reader import ProcessOutputReader, MyConsole
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from ui.LabeledInput import LabeledInput
from ui.DataframeReader import DataframeReader
from ui.layout_cleaner import clean_layout
import numpy as np 
from file import make_train_test_data_files

class FormulaLearner(QMainWindow):

    def __init__(self, reader, parent=None):
        super(FormulaLearner, self).__init__(parent)
        self.reader = reader

        self.widget = QWidget()
        self.layout = QVBoxLayout(self.widget)

        self._process_reader = ProcessOutputReader()
        self.console = MyConsole()
        self.input_layout = QHBoxLayout()
        self.cycles_input = LabeledInput("Ilość cykli:", "20").add_to_layout(self.input_layout)
        self.formulas_input = LabeledInput("Ilość formuł: ", "100").add_to_layout(self.input_layout)
        self.clauses_input = LabeledInput("Ilość klauzul: ", "5").add_to_layout(self.input_layout)
        self.literals_input = LabeledInput("Ilość literałów: ", "3").add_to_layout(self.input_layout)

        self.start_button = QPushButton("Rozpocznij uczenie")
        self.start_button.resize(50,50)
        self.start_button.clicked.connect(self.start_formula_learning)
        self.stop_button = QPushButton("Zakończ proces uczenia")
        self.stop_button.resize(50,50)
        self.stop_button.clicked.connect(self.stop_formula_learning)

        self.button_layout = QHBoxLayout()

        self.button_layout.addWidget(self.start_button)
        self.button_layout.addWidget(self.stop_button)

        self.layout.addLayout(self.button_layout)
        self.layout.addLayout(self.input_layout)
        self.layout.addWidget(self.console)

        self.setCentralWidget(self.widget)
        
        make_train_test_data_files(self.reader.df, self.reader.target_column)

                
    def stop_formula_learning(self):
        self._process_reader.kill()
        self.console.append_output("Process stopped...")

    def start_formula_learning(self):
        self.console.clear_output()
        self._process_reader.produce_output.connect(self.console.append_output)


        """
        variables = {
            "TRAIN_FILE_NAME": "../train.txt",
            "TEST_FILE_NAME": "../test.txt",
            "FORMULAS_COUNT": self.formulas_input.get_value(),
            "CYCLES_COUNT": self.cycles_input.get_value(),
            "CLAUSES_COUNT": self.clauses_input.get_value(),
            "LITERALS_COUNT": self.literals_input.get_value()
        }
        cmd = "run"
        for variable in variables:
            cmd += " -e "+variable+'="'+variables[variable]+'" '
        cmd += "random-learning"

        self._process_reader.start('docker', [
            cmd 
        ])
        """
        
        self._process_reader.start('./core/build/learning_formulas', [
            'train.txt',
            'test.txt',
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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manager uczenia formuł logicznych")
        self.setGeometry(100, 100, 1270, 720)
    
        self.widget = QWidget()
        self.layout = QVBoxLayout(self.widget)
        self.data_layout = QVBoxLayout()
        self.layout.setContentsMargins(5,5,5,5)

        self.selected_file = None 
        self.button_layout = QHBoxLayout()
        self.file_dialog = QFileDialog()
        self.file_dialog.setFileMode(QFileDialog.AnyFile)

        self.load_file = QPushButton("Załaduj plik z danymi csv")
        self.load_file.setFixedWidth(200)
        self.load_file.clicked.connect(self.open_file_dialog)

        self.button_layout.addWidget(self.load_file)

        self.layout.addLayout(self.button_layout)
        self.layout.addLayout(self.data_layout)
        
        # set the central widget of the main window to the new widget
        self.setCentralWidget(self.widget)

    def reload(self):
        self.dialog = FormulaLearner(self.reader)
        self.dialog.show()

    def open_file_dialog(self):
        self.file_dialog = QFileDialog()
        self.file_dialog.setFileMode(QFileDialog.AnyFile)
        self.file_dialog.exec_()
        self.selected_file = self.file_dialog.selectedFiles()[0]
        clean_layout(self.data_layout)

        try:
            self.reader = DataframeReader(self.selected_file, self.data_layout, self)
        except Exception as ex:
            print(ex)
            print("Failed to load file")

app = QApplication(sys.argv)
main_window = MainWindow()

#main_window.start_formula_learning()
main_window.show()
sys.exit(app.exec_())