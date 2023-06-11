import pandas as pd
from PyQt5.QtWidgets import *
from ui.DataframeTableModel import TableModel
from PyQt5.QtCore import Qt
from preprocessing.decimal_encoding.DecimalEncoder import DecimalEncoder
from preprocessing.object_tagging.ObjectTagger import ObjectTagger
from preprocessing.standarizer.Standarizer import Standarizer
from ui.layout_cleaner import clean_layout
from enums.DataEncodingState import DataEncodingState
from ui.state.EncodingState import EncodingState
from preprocessing.DataManager import DataManager
from ui.ColumnEncodingManager import ColumnEncodingManager
from preprocessing.missing_values.Treshold import Treshold

class DataframeReader:

    def __init__(self, file_name, config_file, layout, parent):
        self.state = EncodingState(DataEncodingState.FILL_MISSING)
        self.encoded_to_binary = False 
        self.file_name = file_name
        self.config_file = config_file
        self.model = None
        self.layout = layout
        self.main_layout = QVBoxLayout()
        df = pd.read_csv(self.file_name)
        self.parent = parent 
    
        self.target_select_label = QLabel("Wybierz docelową kolumnę: ")
        self.target_select = QComboBox()
        self.target_select.addItems(df.columns)
        self.target_select.currentIndexChanged.connect(self.targetchange)

        self.setDataframe(df)

        self.target_column = self.data_manager.getTarget()
        self.target_index = self.data_manager.getData().columns.get_loc(self.target_column)

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
        self.data_manager.setTarget(self.target_column)
        self.setDataframe(self.data_manager.getData())

    def fix_missing(self):
        self.target_select.setDisabled(True)
        self.state.setState(DataEncodingState.FLOAT_ENCODING)

        df = self.data_manager.getData()
        for column in df.columns:
            self.data_manager.setFillMissing(
                column,
                Treshold(
                    self.column_managers[column].fill_na_treshold.get_value()/100.0,
                    self.column_managers[column].drop_na_treshold.get_value()/100.0
                )
            )
            if self.column_managers[column].drop_checkbox.isChecked():
                self.data_manager.dropColumn(column)

        self.data_manager.fill_missing()

        self.setDataframe(self.data_manager.getData())

    def to_integers(self):
        self.state.setState(DataEncodingState.OBJECT_TAGGING)

        df = self.data_manager.getData()
        for column in df.columns:
            self.data_manager.setMultipier(column, self.column_managers[column].float_encoding.get_value())

        self.data_manager.encode_floats()
        self.setDataframe(self.data_manager.getData())

    def encode_objects(self):
        self.state.setState(DataEncodingState.VALUE_STANDARIZATION)

        df = self.data_manager.getData()
        for column in df.columns:
            self.data_manager.setMaxUniqueObjects(column, self.column_managers[column].max_unique_objects.get_value())

        self.data_manager.encode_objects()
        self.setDataframe(self.data_manager.getData())

    def standarize_value(self):
        df = self.data_manager.getData()
        for column in df.columns:
            if column == self.target_column:
                continue

            self.data_manager.setValueRanges(column, self.column_managers[column].interval_picker.getIntervals())
            self.data_manager.setBoundaries(column, self.column_managers[column].interval_picker.getBoundaries())

        self.data_manager.standarize()
        for column in df.columns:
            if column == self.target_column:
                continue
            
            self.data_manager.setMaxStandarizedValue(column, self.data_manager.df[column].max()+1)
            
        self.setDataframe(self.data_manager.getData())
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
        df = self.data_manager.getData()
        self.column_managers = {}

        for column in df.columns:
            self.column_managers[column] = ColumnEncodingManager(column)
            self.stats_layout.addLayout(self.column_managers[column].init_ui(self.data_manager, self.state))
        
    def make_table(self):
        self.model = TableModel(self.data_manager.getData())
        self.table.setModel(self.model)
        self.table.setMaximumHeight(300)
    
    def setDataframe(self, df):
        self.data_manager = DataManager(df, self.config_file)
        clean_layout(self.main_layout)
        self.init_layout()
        self.table = self.make_table()
        self.main_layout.addWidget(self.table)
        self.layout.addLayout(self.main_layout)
        self.show_stats()
        
