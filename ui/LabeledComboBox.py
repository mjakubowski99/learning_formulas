from PyQt5.QtWidgets import QSpinBox, QLabel

class LabeledComboBox:

    def __init__(self, label, init_value: int):
        self.__label = QLabel(label)
        self.__combo_box = QSpinBox()
        self.__combo_box.setValue(init_value)

    def add_to_layout(self, layout):
        layout.addWidget(self.__label)
        layout.addWidget(self.__combo_box)
        return self
    
    def setValueRange(self, min:int, max: int):
        self.__combo_box.setRange(min,max)
        return self
    
    def get_value(self):
        return self.__combo_box.value()
        