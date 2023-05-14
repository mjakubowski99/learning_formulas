import pandas as pd
from PyQt5.QtWidgets import QWidget, QTableView, QSizePolicy, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QWidget, QPushButton, QComboBox, QMainWindow
from ui.DataframeTableModel import TableModel
from PyQt5.QtCore import Qt
from preprocessing.missing_values.MissingValuesFiller import MissingValuesFiller
from preprocessing.decimal_encoding.DecimalEncoder import DecimalEncoder
from preprocessing.object_tagging.ObjectTagger import ObjectTagger
from preprocessing.standarizer.Standarizer import Standarizer
from ui.ColumnButton import ColumnButton
from ui.layout_cleaner import clean_layout
from ui.IntervalPicker import IntervalPicker
from ui.IntervalPickerButton import IntervalPickerButton
from ui.ColumnWidgetsManager import ColumnWidgetsManager
from enums.DataEncodingState import DataEncodingState
from ui.state.EncodingState import EncodingState

class DataframeReader:

    def __init__(self, file_name, layout, parent):
        self.state = EncodingState(DataEncodingState)
        self.missing_values_filler = None
        self.standarizer = None 
        self.encoded_to_binary = False 
        self.file_name = file_name
        self.model = None
        self.layout = layout
        self.main_layout = QVBoxLayout()
        df = pd.read_csv(self.file_name)
        self.parent = parent 

        self.target_column = df.columns[0]
        self.target_index = 0

        self.target_select_label = QLabel("Wybierz docelową kolumnę: ")
        self.target_select = QComboBox()
        self.target_select.addItems(df.columns)
        self.target_select.currentIndexChanged.connect(self.targetchange)
    
        self.setDataframe(df)
        self.original_df = df.copy()

    def init_layout(self):
        self.main_layout = QVBoxLayout()
        self.scroll = QScrollArea()          
        self.widget = QWidget()                
        self.stats_layout = QHBoxLayout()
        self.widget.setLayout(self.stats_layout)

        #Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
    
        self.table = QTableView()

        self.buttons_layout = QHBoxLayout()

        self.fix_missing_values_button = QPushButton("Uzupełnij brakujące wartości")
        self.to_integers_button = QPushButton("Przekonwertuj na wartości numeryczne")
        self.encode_objects_button = QPushButton("Zakoduj obiekty jako integer")
        self.standarize_value_button = QPushButton("Zakoduj wartości i zapisz do pliku")

        self.fix_missing_values_button.setVisible(self.state.isFillMissing())
        self.to_integers_button.setVisible(self.state.isFloatEncoding())
        self.encode_objects_button.setVisible(self.state.isObjectTagging())
        self.standarize_value_button.setVisible(self.state.isValueStandarization())
        
        self.to_integers_button.clicked.connect(self.to_integers)
        self.fix_missing_values_button.clicked.connect(self.fix_missing)
        self.encode_objects_button.clicked.connect(self.encode_objects)
        self.standarize_value_button.clicked.connect(self.standarize_value)

        self.main_layout.addWidget(self.target_select_label)
        self.main_layout.addWidget(self.target_select)
        self.main_layout.addWidget(self.table)
        self.buttons_layout.addWidget(self.fix_missing_values_button)
        self.buttons_layout.addWidget(self.to_integers_button)
        self.buttons_layout.addWidget(self.encode_objects_button)
        self.buttons_layout.addWidget(self.standarize_value_button)
        self.main_layout.addLayout(self.buttons_layout)
        self.main_layout.addWidget(self.scroll)

    def targetchange(self,i):
        self.target_column = self.target_select.currentText()
        self.target_index = self.target_select.currentIndex()

    def encode_objects(self):
        self.state.setState(DataEncodingState.VALUE_STANDARIZATION)

        tagger = ObjectTagger(self.df.columns)
        df = tagger.process(self.df, self.target_column)
        self.standarizer = Standarizer(df, self.target_column)
        self.setDataframe(tagger.process(self.df, self.target_column))

    def to_integers(self):
        self.state.setState(DataEncodingState.OBJECT_TAGGING)

        decimal_encoder = DecimalEncoder(self.df.columns)
        self.setDataframe(decimal_encoder.process(self.df, self.target_column))

    def fix_missing(self):
        self.target_select.setDisabled(True)

        self.state.setState(DataEncodingState.FLOAT_ENCODING)

        self.filler = MissingValuesFiller(self.df.columns)
        self.setDataframe(self.missing_values_filler.process(self.df, self.target_column))

    def standarize_value(self):
        self.setDataframe(self.standarizer.process(self.df, self.target_column))
        self.parent.reload()

    def reset_dataframe(self):
        self.init_state()
        self.setDataframe(self.original_df)

    def add_to_layout(self, layout):
        self.layout = layout 
        self.table = self.make_table()
        self.main_layout.addWidget(self.table)
        self.layout.addLayout(self.main_layout)

    def show_stats(self):
        if self.encoded_to_binary:
            return
        
        builder = ColumnWidgetsManager(self.state)
        self.column_layout = builder.make(self)

        self.stats_layout.addLayout(self.column_layout)
        self.main_layout.addLayout(self.column_layout)

        """
        for column in self.df.columns:
            column_layout = QVBoxLayout()
            missing_values_count = self.df[column].isnull().sum()

            label = QLabel("Kolumna: "+column)
            missing_values = QLabel("Ilość brakujących wartości: "+str(missing_values_count))
            data_type = QLabel("Typ danych: "+str(self.df[column].dtype))

            button = ColumnButton(self.df, column, "Pokaż histogram")
            column_layout.addWidget(label)
            
            if self.standarizer is not None:
                button = IntervalPickerButton(self.standarizer, column, self.df.columns)
                button.setContentsMargins(0,0,0,0)
                column_layout.addWidget(button)

            if self.missing_values_state:
                column_layout.addWidget(missing_values)

            if self.df[column].dtype.kind in 'biufc':
                min_value = QLabel("Minimalna wartość: {}".format(self.df[column].min()))
                max_value = QLabel("Maksymalna wartość: {}".format(self.df[column].max()))
                mean_value = QLabel("Srednia wartości: {}".format(self.df[column].mean()))

                column_layout.addWidget(min_value)
                column_layout.addWidget(max_value)
                column_layout.addWidget(mean_value)

                
            column_layout.addWidget(data_type)
            column_layout.addWidget(button)

            self.stats_layout.addLayout(column_layout)
        """
        
    def make_table(self):
        self.model = TableModel(self.df)
        self.table.setModel(self.model)
        self.table.setMaximumHeight(300)
    
    def setDataframe(self, df):
        self.df = df
        clean_layout(self.main_layout)
        self.init_layout()
        self.table = self.make_table()
        self.main_layout.addWidget(self.table)
        self.layout.addLayout(self.main_layout)
        self.show_stats()
        
