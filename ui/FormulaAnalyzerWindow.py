from PyQt5.QtWidgets import *
from utils.file import *
from utils.dataframe import *
from preprocessing.DataManager import DataManager
from postprocessing.FormulaPredictor import FormulaPredictor
from postprocessing.FormulaProcessor import FormulaProcessor
from ui.DataframeTableModel import TableModel

class FormulaAnalyzerWindow(QMainWindow):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Analizer formuł logicznych")
        self.setGeometry(100, 100, 1270, 720)
        self.data_file_dialog_button = self.make_file_dialog_button("Wczytaj dane do predykcji...")
        self.data_file_dialog_button.clicked.connect(self.read_data_file)

        self.widget = QWidget()
        self.layout = QVBoxLayout(self.widget)
        self.layout.addWidget(self.data_file_dialog_button)

        self.setCentralWidget(self.widget)

    def build_dataframe(self, data_file, config_file):

        self.data_manager = DataManager(pd.read_csv(data_file), config_file)

        if (len(self.data_manager.df) > 10000):
            self.data_manager.df = self.data_manager.df[0:6000]

        self.predictor = self.make_predictor_for_latest_data()
        results = self.predictor.predict(self.data_manager.df, self.data_manager.config_file)
        self.data_manager.df = target_to_begin(self.data_manager.getData(), self.data_manager.getTarget())
        self.data_manager.df = insert_column_at(self.data_manager.df, 1, str(self.data_manager.getTarget())+"_predicted", results)

        self.score_label = QLabel("Dokładność predykcji: "+str(self.predictor.score))
        self.table = QTableView()
        self.table_model = TableModel(self.data_manager.df)
        self.table.setModel(self.table_model)

        self.layout.addWidget(self.score_label)
        self.layout.addWidget(self.table)

    def read_data_file(self):
        self.open_file_dialog()
        
        data_file = self.get_selected_file()
        config_file = get_config_file_path_from_file_directory(data_file)

        self.build_dataframe(data_file, config_file)

    def make_predictor_for_latest_data(self):
        processor = FormulaProcessor("core/result/result.txt")
        formulas = processor.process()
        return FormulaPredictor(formulas)

    def make_file_dialog_button(self, text: str):
        file_button = QPushButton()
        file_button.setText(text)
        return file_button

    def open_file_dialog(self):
        self.file_dialog = QFileDialog()
        self.file_dialog.setFileMode(QFileDialog.AnyFile)
        self.file_dialog.exec_() 

    def get_selected_file(self):
        return self.file_dialog.selectedFiles()[0]
    

