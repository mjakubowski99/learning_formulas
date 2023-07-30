import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QComboBox, QLabel
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import Qt
from ui.output_reader import ProcessOutputReader, MyConsole
from PyQt5.QtCore import pyqtSlot
from ui.LabeledSpinBox import LabeledSpinBox
from ui.DataframeReader import DataframeReader
from ui.FormulaAnalyzerWindow import FormulaAnalyzerWindow
from ui.layout_cleaner import clean_layout
import numpy as np 
from file import make_train_test_data_files
from utils.file import *
import shutil
import os 

class FormulaLearner(QMainWindow):

    def __init__(self, reader=None, current_algorithm="RANDOM", run_with_docker=True, parent=None):
        super(FormulaLearner, self).__init__(parent)
        self.reader = reader
        self.run_with_docker = run_with_docker
        self.current_algorithm = current_algorithm
        self.setMinimumSize(1280, 720)

        self.widget = QWidget()
        self.layout = QVBoxLayout(self.widget)

        self._process_reader = ProcessOutputReader()
        self.console_layout = QVBoxLayout()
        self.console = MyConsole()
        self.console_layout.addWidget(self.console)

        self.input_layout = QGridLayout()
        self.make()

        self.start_button = QPushButton("Rozpocznij uczenie")
        self.start_button.resize(50,50)
        self.start_button.clicked.connect(self.start_formula_learning)
        self.stop_button = QPushButton("Zakończ proces uczenia")
        self.stop_button.resize(50,50)
        self.stop_button.clicked.connect(self.stop_formula_learning)

        self.button_layout = QHBoxLayout()

        self.button_layout.addWidget(self.start_button)
        self.button_layout.addWidget(self.stop_button)

        self.layout.addLayout(self.input_layout)
        self.layout.addLayout(self.button_layout)
        self.layout.addLayout(self.console_layout)

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

    def get_current_algorithm(self):
        return self.current_algorithm
    
    def make(self):
        if self.get_current_algorithm() == "RANDOM":
            return self.make_for_random_algorithm()
        return self.make_for_evolution_algorithm()

    def make_for_random_algorithm(self):
        self.cycles_input = LabeledSpinBox("Ilość cykli:", 20).add_to_layout(self.input_layout, 0, 0)
        self.formulas_input = LabeledSpinBox("Ilość formuł: ", 100).add_to_layout(self.input_layout, 0, 1)
        self.min_clauses_input = LabeledSpinBox("Minimalna ilość klauzul: ", 5).add_to_layout(self.input_layout, 0, 2)
        self.max_clauses_input = LabeledSpinBox("Maksymalna ilość klauzul: ", 5).add_to_layout(self.input_layout, 1, 0)
        self.min_literals_input = LabeledSpinBox("Minimalna ilość literałów: ", 5).add_to_layout(self.input_layout, 1, 1)
        self.max_literals_input = LabeledSpinBox("Maksymalna ilość literałów: ", 5).add_to_layout(self.input_layout, 1, 2)
        self.positive_responses_percentage_input = LabeledSpinBox("Wymagany % pozytywnych odpowiedzi formuły: ", 40).add_to_layout(self.input_layout, 2, 0).setValueRange(0,100)

    def make_for_evolution_algorithm(self):
        self.populations_count_input = LabeledSpinBox("Ilość populacji:", 20).add_to_layout(self.input_layout, 0, 0)
        self.final_formulas_size_input = LabeledSpinBox("Finalna ilośc formuł:", 100).add_to_layout(self.input_layout, 0, 1)
        self.formulas_input = LabeledSpinBox("Ilość formuł: ", 300).add_to_layout(self.input_layout, 0, 2)
        self.min_clauses_input = LabeledSpinBox("Minimalna ilość klauzul: ", 5).add_to_layout(self.input_layout, 1, 0)
        self.max_clauses_input = LabeledSpinBox("Maksymalna ilość klauzul: ", 5).add_to_layout(self.input_layout, 1, 1)
        self.min_literals_input = LabeledSpinBox("Minimalna ilość literałów: ", 5).add_to_layout(self.input_layout, 1, 2)
        self.max_literals_input = LabeledSpinBox("Maksymalna ilość literałów: ", 5).add_to_layout(self.input_layout, 2, 0)
        self.new_formulas_percentage_input = LabeledSpinBox("Procent oonownie wylosowanych formuł w populacji: ", 100).add_to_layout(self.input_layout, 2, 1).setValueRange(0,100)
        self.crossing_percentage_input = LabeledSpinBox("Procent formuł do krzyżowania: ", 50).add_to_layout(self.input_layout, 2, 2).setValueRange(0,100)
    
    def stop_formula_learning(self):
        self._process_reader.kill()
        self.console.append_output("Process stopped...")

    def set_up_env(self):
        if self.get_current_algorithm() == "EVOLUTION":

            if not self.run_with_docker:
                result_dir = "../result/",
                train_file_name = "../data/train.txt"
                test_file_name = "../data/test.txt"
            else:
                result_dir = "/src/result/",
                train_file_name = "/src/data/train.txt"
                test_file_name = "/src/data/test.txt"

            variables = {
                "ALGORITHM": self.get_current_algorithm(),
                "TRAIN_FILE_NAME": train_file_name,
                "TEST_FILE_NAME": test_file_name,
                "RESULT_DIR": result_dir,
                "MIN_CLAUSES_COUNT": self.min_clauses_input.get_value(),
                "MAX_CLAUSES_COUNT": self.max_clauses_input.get_value(),
                "MIN_LITERALS_COUNT": self.min_literals_input.get_value(),
                "MAX_LITERALS_COUNT": self.max_literals_input.get_value(),
                "POPULATIONS_COUNT": self.populations_count_input.get_value(),
                "POPULATIONS_SIZE": self.formulas_input.get_value(),
                "FINAL_POPULATION_SIZE": self.final_formulas_size_input.get_value(),
                "NEW_FORMULAS_PERCENTAGE": self.new_formulas_percentage_input.get_value()/100.0,
                "CROSSING_PERCENTAGE": self.crossing_percentage_input.get_value()/100.0,
            }

        with open(".env", "w") as f:
            for variable in variables:
                f.write(variable+"="+str(variables[variable])+'\n')
        f.close()

    def start_with_docker(self):
        self.set_up_env()

        if os.path.exists("core/build"):
            shutil.rmtree("core/build")
        self._process_reader.start("docker-compose", ["up", "--build"])

    def start_with_system(self):
        self.set_up_env()

        with open(".env" , "r") as f:
            for line in f.readlines():
                os.environ[line.split("=")[0]] = line.split("=")[1]
        f.close()

        self._process_reader.start("./run.sh")
                

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
        self.button_layout = QVBoxLayout()
        self.button_layout.setAlignment(Qt.AlignCenter)
        self.file_dialog = QFileDialog()
        self.file_dialog.setFileMode(QFileDialog.AnyFile)

        self.load_file = QPushButton("Wybierz plik csv do przetworzenia...")
        self.load_file.setToolTip("Po kliknięciu zostaniesz przeniesiony do interfejsu pozwalającego zakodować dane z pliku csv na binarne")
        
        self.learn_formula_evolution = QPushButton("Przejdz do uczenia formuł...")
        self.learn_formula_evolution.setToolTip("Po kliknięciu zostaniesz przeniesiony do interfejsu pozwalającego uruchomić algorytm uczenia z różnymi parametrami")
        
        self.learn_formula_random = QPushButton("Przejdz do uczenia formuł(algorytm losowy)...")
        self.learn_formula_random.setToolTip("Po kliknięciu zostaniesz przeniesiony do interfejsu pozwalającego uruchomić algorytm uczenia z różnymi parametrami")

        self.formula_analyzer = QPushButton("Wybierz plik csv do predykcji...")
        self.formula_analyzer.setToolTip("Predykcja zostanie dokonana na podstawie formuł znajdujących się w katalogu core/results/result.txt")
        
        self.load_file.setFixedWidth(400)
        self.learn_formula_evolution.setFixedWidth(400)
        self.learn_formula_random.setFixedWidth(400)
        self.formula_analyzer.setFixedWidth(400)

        self.load_file.clicked.connect(self.open_file_dialog)
        self.learn_formula_evolution.clicked.connect(self.reload_evolution)
        self.learn_formula_random.clicked.connect(self.reload_random)
        self.formula_analyzer.clicked.connect(self.analyzer)

        self.button_layout.addWidget(self.load_file)
        self.button_layout.addWidget(self.learn_formula_evolution)
        self.button_layout.addWidget(self.formula_analyzer)

        self.layout.addLayout(self.button_layout)
        self.layout.addLayout(self.data_layout)
        
        # set the central widget of the main window to the new widget
        self.setCentralWidget(self.widget)
        self.reader = None

    def analyzer(self):
        self.dialog = FormulaAnalyzerWindow()
        self.dialog.show()

    def reload_evolution(self):
        self.dialog = FormulaLearner(self.reader, "EVOLUTION", self.run_with_docker)
        self.dialog.show()

    def reload_random(self):
        self.dialog = FormulaLearner(self.reader,  "RANDOM", self.run_with_docker)
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