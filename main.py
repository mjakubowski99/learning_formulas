import sys 
from MainWindow import MainWindow
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)
main_window = MainWindow(False)

#main_window.start_formula_learning()
main_window.show()
sys.exit(app.exec_())