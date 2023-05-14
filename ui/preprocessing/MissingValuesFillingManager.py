from preprocessing.missing_values.MissingValuesFiller import MissingValuesFiller
from preprocessing.missing_values.MissingValuesFiller import MissingValuesFiller
from ui.LabeledSpinBox import LabeledSpinBox

import pandas as pd 
from PyQt5.QtWidgets import *

class MissingValuesFillingManager:

    def __init__(self, filler: MissingValuesFiller = None):
        self.filler = filler 

    def make_widgets(self, df: pd.DataFrame, column, layout: QBoxLayout) -> None:
        self.filler = MissingValuesFiller(df.columns)

        missing_values_count = df[column].isnull().sum()

        if missing_values_count == 0:
            return 
        
        missing_values = QLabel("Ilość brakujących wartości: "+str(missing_values_count))
        fill_na_treshold = LabeledSpinBox("Próg do uzupełnienia wartości: ", 10)
        drop_na_treshold = LabeledSpinBox("Próg do usunięcia wiersza", 40)

        layout.addWidget(missing_values)
        fill_na_treshold.add_to_layout(layout)
        drop_na_treshold.add_to_layout(layout)