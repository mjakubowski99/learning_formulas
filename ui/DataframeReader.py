import pandas as pd
from PyQt5.QtWidgets import QWidget, QTableView, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QScrollArea, QWidget, QPushButton, QComboBox, QMainWindow
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

class DataframeReader:

    def __init__(self, file_name, layout, parent):
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

        self.init_state()
    
        self.setDataframe(df)
        self.original_df = df.copy()

    def init_state(self):
        self.missing_values_state = True
        self.decimal_to_integer_state = False
        self.tag_objects_state = False
        self.standarize_value_state = False

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
        self.table.horizontalHeader().sectionClicked.connect(self.header_clicked)
    
        self.buttons_layout = QHBoxLayout()

        self.fix_missing_values_button = QPushButton("Uzupełnij brakujące wartości")
        self.to_integers_button = QPushButton("Przekonwertuj na wartości numeryczne")
        self.encode_objects_button = QPushButton("Zakoduj obiekty jako integer")
        self.standarize_value_button = QPushButton("Zakoduj wartości i zapisz do pliku")

        self.fix_missing_values_button.setVisible(self.missing_values_state)
        self.to_integers_button.setVisible(self.decimal_to_integer_state)
        self.encode_objects_button.setVisible(self.tag_objects_state)
        self.standarize_value_button.setVisible(self.standarize_value_state)
        
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

    def header_clicked(self, index):
        window = QMainWindow()
        window.setFixedWidth(500)
        window.setFixedHeight(500)
        column_layout = QVBoxLayout()
        widget = QWidget()

        column = self.df.columns[index]
        missing_values_count = self.df[column].isnull().sum()
        label = QLabel("Kolumna: "+column)
        missing_values = QLabel("Ilość brakujących wartości: "+str(missing_values_count))
        data_type = QLabel("Typ danych: "+str(self.df[column].dtype))
        button = ColumnButton(self.df, column, "Pokaż histogram")

        column_layout.setContentsMargins(0,0,0,0)
        column_layout.addWidget(label)
        
        if self.standarizer is not None:
            button = IntervalPickerButton(self.standarizer, column, self.df.columns)
            column_layout.addWidget(button)

        if self.missing_values_state:
            column_layout.addWidget(missing_values)
            
        column_layout.addWidget(data_type)
        column_layout.addWidget(button)

        widget.setLayout(column_layout)
        window.setCentralWidget(widget)
        window.show()

    def targetchange(self,i):
        self.target_column = self.target_select.currentText()
        self.target_index = self.target_select.currentIndex()

    def encode_objects(self):
        self.tag_objects_state = False 
        self.standarize_value_state = True

        tagger = ObjectTagger(self.df.columns)
        df = tagger.process(self.df, self.target_column)
        self.standarizer = Standarizer(df, self.target_column)
        self.setDataframe(tagger.process(self.df, self.target_column))

    def to_integers(self):
        self.decimal_to_integer_state = False
        self.tag_objects_state = True

        decimal_encoder = DecimalEncoder(self.df.columns)
        self.setDataframe(decimal_encoder.process(self.df, self.target_column))

    def fix_missing(self):
        self.target_select.setDisabled(True)
        self.decimal_to_integer_state = True
        self.missing_values_state = False

        filler = MissingValuesFiller(self.df.columns)
        self.setDataframe(filler.process(self.df, self.target_column))

    def standarize_value(self):
        self.setDataframe(self.standarizer.process(self.df, self.target_column))
        print(self.df)
        self.parent.reload()

    def reset_dataframe(self):
        self.init_state()
        self.setDataframe(self.original_df)

    def add_to_layout(self, layout):
        self.layout = layout 
        self.table = self.make_table()
        self.main_layout.addWidget(self.table)
        self.layout.addLayout(self.main_layout)
        
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
        
