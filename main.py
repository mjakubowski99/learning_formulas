import sys 
from MainWindow import MainWindow
from PyQt5.QtWidgets import QApplication

run_with_docker = False

app = QApplication(sys.argv)
main_window = MainWindow(run_with_docker)

main_window.show()
sys.exit(app.exec_())