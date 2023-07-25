from PyQt5.QtWidgets import QSpinBox, QLabel, QVBoxLayout

class LabeledSpinBox:

    def __init__(self, label, init_value: int):
        self.layout = QVBoxLayout()
        self.__label = QLabel(label)
        self.__spin_box = QSpinBox()
        self.setValueRange(0,1000000)
        self.__spin_box.setValue(init_value)

    def add_to_layout(self, layout, row=None, column=None):
        self.layout.addWidget(self.__label)
        self.layout.addWidget(self.__spin_box)

        if row is not None and column is not None:
            layout.addLayout(self.layout, row, column)
        else:
            layout.addLayout(self.layout)

        return self
    
    def setValueRange(self, min:int, max: int):
        self.__spin_box.setRange(min,max)
        return self
    
    def get_spin_box(self) -> QSpinBox:
        return self.__spin_box
    
    def get_value(self):
        return self.__spin_box.value()
        