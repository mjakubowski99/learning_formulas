from PyQt5.QtWidgets import QPushButton
from ui.output_reader import ProcessOutputReader, MyConsole

class LearningManager:

    def __init__(self):
        self._process_reader = ProcessOutputReader()
        self.console = MyConsole()
        self.start_button = QPushButton("Rozpocznij uczenie")
        self.stop_button = QPushButton("Zakończ proces uczenia")
        self.cycles_count = 20
        self.formulas_count = 100
        self.clauses_count = 5
        self.literals_count = 3
        self.positive_responses_percentage = 0.4

    def set_params(self, cycles_count, formulas_count, clauses_count, literals_count):
        self.cycles_count = cycles_count
        self.formulas_count = formulas_count
        self.clauses_count = clauses_count
        self.literals_count = literals_count
    
    def add_buttons_to_layout(self, layout):
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)

    def add_process_reader_to_layout(self, layout):
        layout.addWidget(self.console)

    def start_formula_learning(self):
        self.console.clear_output()
        self._process_reader.produce_output.connect(self.console.append_output)
        self._process_reader.start('./core/build/learning_formulas', [
            'core/data/train.txt',
            'core/data/test.txt',
            self.cycles_count,
            self.formulas_count,
            self.clauses_count,
            self.literals_count,
            "core/result/"
        ])

    def stop_formula_learning(self):
        self._process_reader.kill()
        self.console.append_output("Process stopped...")