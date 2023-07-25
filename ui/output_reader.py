import sys

from PyQt5.QtCore import pyqtSignal, pyqtSlot, QProcess, QTextCodec
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QApplication, QPlainTextEdit

class ProcessOutputReader(QProcess):
    produce_output = pyqtSignal(str)
    process_finished = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setProcessChannelMode(QProcess.MergedChannels)
        codec = QTextCodec.codecForLocale()
        self._decoder_stdout = codec.makeDecoder()
        self.readyReadStandardOutput.connect(self._ready_read_standard_output)
        self.finished.connect(self._process_finished)

    @pyqtSlot()
    def _ready_read_standard_output(self):
        raw_bytes = self.readAllStandardOutput()
        text = self._decoder_stdout.toUnicode(raw_bytes)
        self.produce_output.emit(text)

    @pyqtSlot()
    def _process_finished(self):
        self.process_finished.emit()

class MyConsole(QPlainTextEdit):

    def __init__(self, parent=None):
        super().__init__()
        self.setMaximumBlockCount(10000)  # limit console to 10000 lines
        self._cursor_output = self.textCursor()

    def clear_output(self):
        self.clear()

    @pyqtSlot(str)
    def append_output(self, text):
        self._cursor_output.insertText(text)
        self.scroll_to_last_line()

    def scroll_to_last_line(self):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.movePosition(QTextCursor.Up if cursor.atBlockStart() else QTextCursor.StartOfLine)
        self.setTextCursor(cursor)