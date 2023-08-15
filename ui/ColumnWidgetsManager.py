import pandas as pd
from ui.state.EncodingState import EncodingState
from PyQt5.QtWidgets import *
from processing.preprocessing.MissingValuesFiller import MissingValuesFiller
from ui.ColumnButton import ColumnButton
from ui.DataframeReader import DataframeReader
from ui.ColumnActionButton import ColumnActionButton

class ColumnWidgetsManager:

    def __init__(self, state: EncodingState):
        self.state = state
        self.dataframe_reader = None
        self.layout = QHBoxLayout()
        self.missing_values_filler = MissingValuesFiller()

    def make(self, dataframe_reader: DataframeReader) -> QBoxLayout:
        self.dataframe_reader = dataframe_reader
        df = self.dataframe_reader.df

        for column in df:
            self.layout.addLayout(self.make_for_column(df, column))
        return self.layout
            
    def make_for_column(self, df: pd.DataFrame, column) -> QBoxLayout:
        layout = QVBoxLayout()
        self.__make_label(column, layout)
        self.__make_drop_column_button(column, layout)

        if self.state.isFillMissing():
            self.missing_values_filling_manager.make_widgets(df, column, layout)

        self.__make_histogram_widget(df, column, layout)

        return layout
        
    def __make_label(self, column, layout: QBoxLayout) -> None:
        self.label = QLabel("Kolumna: "+column)
        layout.addWidget(self.label)

    def __make_drop_column_button(self, column, layout: QBoxLayout) -> None:
        drop_column = ColumnActionButton("Usuń kolumnę", column)
        drop_column.clicked.connect(self.__on_drop_column)
        layout.addWidget(drop_column)

    def __make_histogram_widget(self, df: pd.DataFrame, column, layout: QBoxLayout):
        button = ColumnButton(df, column, "Pokaż histogram")
        layout.addWidget(button)

    def __on_drop_column(self, button: ColumnActionButton):
        df = self.dataframe_reader.df 
        self.dataframe_reader.setDataframe(df.drop(columns=[button.column]))

        




    

        
        
        