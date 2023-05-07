from models.Interval import Interval
from PyQt5.QtWidgets import QSpinBox, QLabel
from PyQt5.QtWidgets import QTableView, QHBoxLayout

class IntervalPicker:
    def __init__(self, intervals: dict[int, Interval]):
        self.intervals = intervals
        self.pickers = {}

        self.max = 0
        self.min = 0
        for id, interval in self.intervals.items():
            if interval.end > self.max:
                self.max = interval.end
            if interval.begin < self.min:
                self.min = interval.begin

        for id, interval in self.intervals.items():
            self.pickers[id] = self.make_picker(id, interval)

    def get_from_picker(self):
        intervals = {}
        for id, picker in self.pickers.items():
            intervals[id] = Interval(picker['min'].value(), picker['max'].value())
        return intervals

    def add_to_layout(self, layout):
        for id, pickers in self.pickers.items():
            picker_layout = QHBoxLayout()
            picker_layout.addWidget(QLabel("Wartość: "+str(id)))
            picker_layout.addWidget(pickers['min'])
            picker_layout.addWidget(pickers['max'])
            layout.addLayout(picker_layout)
            

    def make_picker(self, identifier: int, interval: Interval):
        pickers = {}
        pickers['min'] = QSpinBox()
        pickers['max'] = QSpinBox()
        pickers['min'].wheelEvent = lambda event: None
        pickers['max'].wheelEvent = lambda event: None

        pickers['min'].value()

        pickers['min'].setMinimum(self.min)
        pickers['min'].setMaximum(self.max)

        pickers['max'].setMinimum(self.min)
        pickers['max'].setMaximum(self.max)

        pickers['min'].setValue(interval.begin)
        pickers['max'].setValue(interval.end)

        return pickers  
