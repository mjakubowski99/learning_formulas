import pandas as pd
from PyQt5.QtWidgets import QTableView, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QWidget, QPushButton, QComboBox
from ui.DataframeTableModel import TableModel
from PyQt5.QtCore import QSize
from PyQt5.QtCore import Qt, QSize
from preprocessing.missing_values_adder import fill_missing
from preprocessing.encode_decimal_to_integers import encode_decimal_to_integers
from preprocessing.tag_objects import tag_objects
from preprocessing.to_binary import to_binary

from ui.layout_cleaner import clean_layout

class DataframeReader:

    def __init__(self, file_name, layout, parent):
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
        self.stats_layout = QVBoxLayout()
        self.widget.setLayout(self.stats_layout)

        #Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
    
        self.table = QTableView()

        self.buttons_layout = QHBoxLayout()

        self.fix_missing_values_button = QPushButton("Uzupełnij brakujące wartości")
        self.to_integers_button = QPushButton("Przekonwertuj na wartości numeryczne")
        self.encode_objects_button = QPushButton("Zakoduj obiekty jako integer")
        self.cast_to_binary_button = QPushButton("Zmień na wartości binarne")
        
    
        self.to_integers_button.clicked.connect(self.to_integers)
        self.fix_missing_values_button.clicked.connect(self.fix_missing)
        self.encode_objects_button.clicked.connect(self.encode_objects)
        self.cast_to_binary_button.clicked.connect(self.cast_to_binary)

        self.main_layout.addWidget(self.target_select_label)
        self.main_layout.addWidget(self.target_select)
        self.main_layout.addWidget(self.table)
        self.buttons_layout.addWidget(self.fix_missing_values_button)
        self.buttons_layout.addWidget(self.to_integers_button)
        self.buttons_layout.addWidget(self.encode_objects_button)
        self.buttons_layout.addWidget(self.cast_to_binary_button)
        self.main_layout.addLayout(self.buttons_layout)
        self.main_layout.addWidget(self.scroll)

    def targetchange(self,i):
        self.target_column = self.target_select.currentText()
        self.target_index = self.target_select.currentIndex()

    def encode_objects(self):
        self.setDataframe(tag_objects(self.df))

    def to_integers(self):
        self.setDataframe(encode_decimal_to_integers(self.df))

    def fix_missing(self):
        self.setDataframe(fill_missing(self.df, self.target_column))

    def cast_to_binary(self):
        self.encoded_to_binary = True 
        self.setDataframe(to_binary(self.df, self.target_column))
        self.parent.reload()

    def reset_dataframe(self):
        self.setDataframe(self.original_df)

    def show_stats(self):
        if self.encoded_to_binary:
            return
        
        for column in self.df.columns:
            missing_values_count = self.df[column].isnull().sum()

            label = QLabel("Kolumna: "+column)
            missing_values = QLabel("Ilość brakujących wartości: "+str(missing_values_count))
            data_type = QLabel("Typ danych: "+str(self.df[column].dtype))

            self.stats_layout.addWidget(label)
            self.stats_layout.addWidget(missing_values)
            self.stats_layout.addWidget(data_type)

        self.main_layout.addLayout(self.stats_layout)

    def add_to_layout(self, layout):
        self.layout = layout 
        self.table = self.make_table()
        self.main_layout.addWidget(self.table)
        self.show_stats()
        self.layout.addLayout(self.main_layout)
        
    def make_table(self):
        self.model = TableModel(self.df)
        self.table.setModel(self.model)
        self.table.setMaximumHeight(300)
    
    def setDataframe(self, df):
        self.df = df.copy()
        clean_layout(self.main_layout)
        self.init_layout()
        self.table = self.make_table()
        self.main_layout.addWidget(self.table)
        self.show_stats()
        self.layout.addLayout(self.main_layout)
        
