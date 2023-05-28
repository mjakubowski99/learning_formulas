from ui.state.EncodingState import EncodingState
from ui.IntervalPickerButton import IntervalPickerButton
from ui.LabeledSpinBox import LabeledSpinBox
from ui.ColumnButton import ColumnButton
from ui.ColumnCheckbox import ColumnCheckbox
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
            column_layout.addWidget(self.drop_checkbox)

        elif state.isFloatEncoding():
            self.__init_float_multipliers(data_manager, state)
            self.float_encoding.add_to_layout(column_layout)

        elif state.isObjectTagging():
            self.__init_max_unique_objects(data_manager, state)
            self.max_unique_objects.add_to_layout(column_layout)

        elif state.isValueStandarization():
            data_manager.init_standarizer()
            self.__init_interval_picker(data_manager, state)
            column_layout.addWidget(self.interval_picker)

        column_layout.addWidget(self.hist_button)

        return column_layout

    def __init_defaults(self, df: pd.DataFrame, state: EncodingState):
        self.label = QLabel("Kolumna: "+self.column)
        self.data_type = QLabel("Typ danych: "+str(df[self.column].dtype))
        self.hist_button = ColumnButton(df, self.column, "Pokaż histogram")

    def __init_missing_values_count(self, data_manager: DataManager, state: EncodingState):
        df = data_manager.getData()

        missing_values_percentage = df[self.column].isnull().sum() / len(df[self.column])
        self.missing_values_count = QLabel("Ilość brakujących wartości: {}".format(round(missing_values_percentage,2)))

        self.drop_checkbox = ColumnCheckbox(self.column)
        self.drop_checkbox.setText("Kolumna do usunięcia")
        self.drop_checkbox.setChecked(data_manager.columnDropped(self.column))
        self.fill_na_treshold = LabeledSpinBox(
            "Próg do uzupełnienia wartości:", 
            round(data_manager.getFillMissing(self.column)['fill_na_treshold']*100)
        )
        self.drop_na_treshold = LabeledSpinBox(
            "Próg do usunięcia wartości:", 
            round(data_manager.getFillMissing(self.column)['drop_na_treshold']*100)
        )

    def __init_float_multipliers(self, data_manager: DataManager, state: EncodingState):
        df = data_manager.getData()

        self.float_encoding = LabeledSpinBox(
            "Mnożnik wartości float:",
            data_manager.getMultipier(self.column)
        )
        self.float_encoding.setValueRange(0,100000000)

    def __init_max_unique_objects(self, data_manager: DataManager, state: EncodingState):
        self.max_unique_objects = LabeledSpinBox(
            "Maksymalna ilość unikalnych wartości:",
            data_manager.getMaxUniqueObjects(self.column)
        )
        self.max_unique_objects.setValueRange(0,100000000)

    def __init_interval_picker(self, data_manager: DataManager, state: EncodingState):
        self.interval_picker = IntervalPickerButton(data_manager.value_standarizer, self.column, data_manager.getData().columns)




