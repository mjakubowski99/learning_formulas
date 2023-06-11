import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox
from PyQt5.QtWidgets import QFileDialog
from ui.output_reader import ProcessOutputReader, MyConsole
from PyQt5.QtCore import pyqtSlot
from ui.LabeledSpinBox import LabeledSpinBox
from ui.DataframeReader import DataframeReader
from ui.FormulaAnalyzerWindow import FormulaAnalyzerWindow
from ui.layout_cleaner import clean_layout
import numpy as np 
from file import make_train_test_data_files
from utils.file import *

class FormulaLearner(QMainWindow):

    def __init__(self, reader=None, run_with_docker=True, parent=None):
        super(FormulaLearner, self).__init__(parent)
        self.reader = reader
        self.run_with_docker = run_with_docker

        self.widget = QWidget()
        self.layout = QVBoxLayout(self.widget)

        self._process_reader = ProcessOutputReader()
        self.console = MyConsole()
        self.select_layout = QHBoxLayout()
        self.make_select()

        self.input_layout = QHBoxLayout()
        self.make_for_random_algorithm()

        self.start_button = QPushButton("Rozpocznij uczenie")
        self.start_button.resize(50,50)
        self.start_button.clicked.connect(self.start_formula_learning)
        self.stop_button = QPushButton("Zakończ proces uczenia")
        self.stop_button.resize(50,50)
        self.stop_button.clicked.connect(self.stop_formula_learning)

        self.button_layout = QHBoxLayout()

        self.button_layout.addWidget(self.start_button)
        self.button_layout.addWidget(self.stop_button)

        self.layout.addLayout(self.select_layout)
        self.layout.addLayout(self.button_layout)
        self.layout.addLayout(self.input_layout)
        self.layout.addWidget(self.console)

        self.setCentralWidget(self.widget)

        self.train_file = "core/data/train.txt"
        self.test_file = "core/data/test.txt"
        
        if reader is not None:
            make_train_test_data_files(
                self.reader.data_manager.getData(), 
                self.reader.target_column, 
                self.train_file,
                self.test_file
            )

    def make_select(self):
        self.algorithm_selector = QComboBox()
        self.algorithm_selector.addItems(['Randomowy', 'Ewolucyjny'])
        self.algorithm_selector.currentIndexChanged.connect(self.on_selected_algorithm)
        self.select_layout.addWidget(self.algorithm_selector)

    def get_current_algorithm(self):
        if self.algorithm_selector.currentIndex() == 0:
            return "RANDOM"
        return "EVOLUTION"

    def on_selected_algorithm(self):
        for i in range(self.input_layout.count()): 
            self.input_layout.itemAt(i).widget().close()

        if self.get_current_algorithm() == "RANDOM":
            self.make_for_random_algorithm()
        else:
            self.make_for_evolution_algorithm()

    def make_for_random_algorithm(self):
        self.cycles_input = LabeledSpinBox("Ilość cykli:", 20).add_to_layout(self.input_layout)
        self.formulas_input = LabeledSpinBox("Ilość formuł: ", 100).add_to_layout(self.input_layout)
        self.min_clauses_input = LabeledSpinBox("Minimalna ilość klauzul: ", 5).add_to_layout(self.input_layout)
        self.max_clauses_input = LabeledSpinBox("Maksymalna ilość klauzul: ", 5).add_to_layout(self.input_layout)
        self.min_literals_input = LabeledSpinBox("Minimalna ilość literałów: ", 5).add_to_layout(self.input_layout)
        self.max_literals_input = LabeledSpinBox("Maksymalna ilość literałów: ", 5).add_to_layout(self.input_layout)
        self.positive_responses_percentage_input = LabeledSpinBox("Wymagany % pozytywnych odpowiedzi formuły: ", 40).add_to_layout(self.input_layout).setValueRange(0,100)

    def make_for_evolution_algorithm(self):
        self.populations_count_input = LabeledSpinBox("Ilość populacji:", 20).add_to_layout(self.input_layout)
        self.final_formulas_size_input = LabeledSpinBox("Finalna ilośc formuł:", 100).add_to_layout(self.input_layout)
        self.formulas_input = LabeledSpinBox("Ilość formuł: ", 300).add_to_layout(self.input_layout)
        self.min_clauses_input = LabeledSpinBox("Minimalna ilość klauzul: ", 5).add_to_layout(self.input_layout)
        self.max_clauses_input = LabeledSpinBox("Maksymalna ilość klauzul: ", 5).add_to_layout(self.input_layout)
        self.min_literals_input = LabeledSpinBox("Minimalna ilość literałów: ", 5).add_to_layout(self.input_layout)
        self.max_literals_input = LabeledSpinBox("Maksymalna ilość literałów: ", 5).add_to_layout(self.input_layout)
        self.mutations_percentage_input = LabeledSpinBox("Procent mutacji: ", 5).add_to_layout(self.input_layout).setValueRange(0,100)
        self.percentage_to_reproduce_input = LabeledSpinBox("Procent populacji do reporodukcji: ", 50).add_to_layout(self.input_layout).setValueRange(0,100)

    def stop_formula_learning(self):
        self._process_reader.kill()
        self.console.append_output("Process stopped...")

    def set_up_env(self):
        if self.get_current_algorithm() == "RANDOM":
            variables = {
                "ALGORITHM": self.get_current_algorithm(),
                "TRAIN_FILE_NAME": "/src/data/train.txt",
                "TEST_FILE_NAME": "/src/data/test.txt",
                "RESULT_DIR": "/src/result/",
                "FORMULAS_COUNT": self.formulas_input.get_value(),
                "CYCLES_COUNT": self.cycles_input.get_value(),
                "MIN_CLAUSES_COUNT": self.min_clauses_input.get_value(),
                "MAX_CLAUSES_COUNT": self.max_clauses_input.get_value(),
                "MIN_LITERALS_COUNT": self.min_literals_input.get_value(),
                "MAX_LITERALS_COUNT": self.max_literals_input.get_value(),
                "POSITIVE_RESPONSES_PERCENTAGE": self.positive_responses_percentage_input.get_value(),
            }
        else:
            variables = {
                "ALGORITHM": self.get_current_algorithm(),
                "TRAIN_FILE_NAME": "/src/data/train.txt",
                "TEST_FILE_NAME": "/src/data/test.txt",
                "RESULT_DIR": "/src/result/",
                "MIN_CLAUSES_COUNT": self.min_clauses_input.get_value(),
                "MAX_CLAUSES_COUNT": self.max_clauses_input.get_value(),
                "MIN_LITERALS_COUNT": self.min_literals_input.get_value(),
                "MAX_LITERALS_COUNT": self.max_literals_input.get_value(),
                "POPULATIONS_COUNT": self.populations_count_input.get_value(),
                "POPULATIONS_SIZE": self.formulas_input.get_value(),
                "FINAL_POPULATION_SIZE": self.final_formulas_size_input.get_value(),
                "MUTATION_PERCENTAGE": self.mutations_percentage_input.get_value()/100.0,
                "REPRODUCTION_PERCENTAGE": self.percentage_to_reproduce_input.get_value()/100.0
            }

        with open(".env", "w") as f:
            for variable in variables:
                f.write(variable+"="+str(variables[variable])+'\n')
        f.close()

    def start_with_docker(self):
        self.set_up_env()
        self._process_reader.start("docker-compose", ["up", "--build"])

    def start_with_system(self):
        self._process_reader.start('./core/build/learning_formulas', [
            self.train_file,
            self.test_file,
            self.cycles_input.get_value(),
            self.formulas_input.get_value(),
            self.clauses_input.get_value(),
            self.literals_input.get_value(),
        ])


    def start_formula_learning(self):
        self.console.clear_output()
        self._process_reader.produce_output.connect(self.console.append_output)

        if self.run_with_docker:
            self.start_with_docker()
        else:
            self.start_with_system()

    @pyqtSlot()
    def _delete_process_reader(self):
        self.layout.removeWidget(self.console)
        self.console.setParent(None)


class MainWindow(QMainWindow):
    def __init__(self, run_with_docker=True):
        super().__init__()
        self.setWindowTitle("Manager uczenia formuł logicznych")
        self.setGeometry(100, 100, 1270, 720)

        self.run_with_docker = run_with_docker
    
        self.widget = QWidget()
        self.layout = QVBoxLayout(self.widget)
        self.data_layout = QVBoxLayout()
        self.layout.setContentsMargins(5,5,5,5)

        self.selected_file = None 
        self.button_layout = QHBoxLayout()
        self.file_dialog = QFileDialog()
        self.file_dialog.setFileMode(QFileDialog.AnyFile)

        self.load_file = QPushButton("Załaduj plik z danymi csv")
        self.learn_formula = QPushButton("Przejdz do uczenia formuł...")
        self.formula_analyzer = QPushButton("Przejdź do analizy formuł...")
        self.load_file.setFixedWidth(200)
        self.learn_formula.setFixedWidth(200)
        self.load_file.clicked.connect(self.open_file_dialog)
        self.learn_formula.clicked.connect(self.reload)
        self.formula_analyzer.clicked.connect(self.analyzer)

        self.button_layout.addWidget(self.load_file)
        self.button_layout.addWidget(self.learn_formula)
        self.button_layout.addWidget(self.formula_analyzer)

        self.layout.addLayout(self.button_layout)
        self.layout.addLayout(self.data_layout)
        
        # set the central widget of the main window to the new widget
        self.setCentralWidget(self.widget)
        self.reader = None

    def analyzer(self):
        self.dialog = FormulaAnalyzerWindow()
        self.dialog.show()

    def reload(self):
        self.dialog = FormulaLearner(self.reader, self.run_with_docker)
        self.dialog.show()

    def open_file_dialog(self):
        self.file_dialog = QFileDialog()
        self.file_dialog.setFileMode(QFileDialog.AnyFile)
        self.file_dialog.exec_()
        self.selected_file = self.file_dialog.selectedFiles()[0]
        clean_layout(self.data_layout)

        self.config_file = get_config_file_path_from_file_directory(self.selected_file)

        try:
            self.reader = DataframeReader(self.selected_file, self.config_file, self.data_layout, self)
        except Exception as ex:
            print("Failed to load file")
            raise ex