from ui.state.EncodingState import EncodingState
from ui.LabeledSpinBox import LabeledSpinBox
from ui.ColumnButton import ColumnButton
from ui.ColumnActionButton import ColumnActionButton
from preprocessing.DataManager import DataManager
from PyQt5.QtWidgets import *
import pandas as pd

class ColumnEncodingManager:

    def __init__(self, column):
        self.column = column

    def init_ui(self, data_manager: DataManager, state: EncodingState) -> QBoxLayout:
        df = data_manager.getData()
        column_layout = QVBoxLayout()

        self.__init_defaults(df, state)
        column_layout.addWidget(self.label)
        column_layout.addWidget(self.data_type)

        if state.isFillMissing():
            self.__init_missing_values_count(data_manager, state)
            column_layout.addWidget(self.missing_values_count)
            self.fill_na_treshold.add_to_layout(column_layout)
            self.drop_na_treshold.add_to_layout(column_layout)
            column_layout.addWidget(self.drop_column)

        column_layout.addWidget(self.hist_button)

        return column_layout

    def __init_defaults(self, df: pd.DataFrame, state: EncodingState):
        self.label = QLabel("Kolumna: "+self.column)
        self.data_type = QLabel("Typ danych: "+str(df[self.column].dtype))
        self.hist_button = ColumnButton(df, self.column, "Pokaż histogram")
        self.drop_column = ColumnActionButton(self.column)
        self.drop_column.setText("Usuń kolumnę")

    def __init_missing_values_count(self, data_manager: DataManager, state: EncodingState):
        df = data_manager.getData()

        missing_values_percentage = df[self.column].isnull().sum() / len(df[self.column])
        self.missing_values_count = QLabel("Ilość brakujących wartości: {}".format(round(missing_values_percentage,2)))

        self.fill_na_treshold = LabeledSpinBox(
            "Próg do uzupełnienia wartości:", 
            round(data_manager.getFillMissing(self.column)['fill_na_treshold']*100)
        )
        self.drop_na_treshold = LabeledSpinBox(
            "Próg do usunięcia wartości:", 
            round(data_manager.getFillMissing(self.column)['drop_na_treshold']*100)
        )




