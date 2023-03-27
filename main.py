import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QSlider
from ui.output_reader import ProcessOutputReader, MyConsole
from PyQt5.QtCore import pyqtSignal, pyqtSlot

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 1270, 720)
        
        # create a new widget and layou
        widget = QWidget()
        self.layout = QVBoxLayout(widget)
        button = QPushButton("Click", self)
        slider = QSlider()
        
        # create a MyConsole widget and add it to the layout
        self._process_reader = ProcessOutputReader()
        self._process_reader.process_finished.connect(self._delete_process_reader)
        self.console = MyConsole()
        app = QApplication.instance()
        app.aboutToQuit.connect(self.closeEvent)

        self.layout.addWidget(button)
        self.layout.addWidget(slider)
        self.layout.addWidget(self.console)
        
        # set the central widget of the main window to the new widget
        self.setCentralWidget(widget)

    @pyqtSlot()
    def _delete_process_reader(self):
        self.layout.removeWidget(self.console)
        self.console.setParent(None)

    def closeEvent(self, event):
        self._process_reader.kill() # zabij proces Docker


app = QApplication(sys.argv)
main_window = MainWindow()
main_window._process_reader.produce_output.connect(main_window.console.append_output)
main_window._process_reader.start('docker-compose', ['up'])
main_window.show()
sys.exit(app.exec_())