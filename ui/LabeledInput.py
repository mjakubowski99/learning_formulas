from PyQt5.QtWidgets import QLineEdit, QLabel

class LabeledInput:

    def __init__(self, label, init_value=""):
        self.label = QLabel(label)
        self.input = QLineEdit(init_value)

    def add_to_layout(self, layout):
        layout.addWidget(self.label)
        layout.addWidget(self.input)
        return self
    
    def get_value(self):
        return str(int(self.input.text()))
        