from PyQt5.QtWidgets import QSpinBox, QLabel

class LabeledSpinBox:

    def __init__(self, label, init_value: int):
        self.__label = QLabel(label)
        self.__spin_box = QSpinBox()
        self.__spin_box.setValue(init_value)

    def add_to_layout(self, layout):
        layout.addWidget(self.__label)
        layout.addWidget(self.__spin_box)
        return self
    
    def setValueRange(self, min:int, max: int):
        self.__spin_box.setRange(min,max)
        return self
    
    def get_spin_box(self) -> QSpinBox:
        return self.__spin_box
    
    def get_value(self):
        return self.__spin_box.value()
        