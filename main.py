import sys 
from ui.MainWindow import MainWindow
from PyQt5.QtWidgets import QApplication

run_with_docker = True

app = QApplication(sys.argv)
main_window = MainWindow(run_with_docker)

main_window.show()
sys.exit(app.exec_())