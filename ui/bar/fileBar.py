# ui/bar/fileBar.py
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt5.QtCore import pyqtSignal

class FileBar(QWidget):
    loadDxfClicked = pyqtSignal()
    loadLogClicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.btnLoadDxf = QPushButton("도면 불러오기")
        self.btnLoadLog = QPushButton("로그 불러오기")

        layout.addWidget(self.btnLoadDxf)
        layout.addWidget(self.btnLoadLog)
        layout.addStretch(1)

        self.btnLoadDxf.clicked.connect(self.loadDxfClicked.emit)
        self.btnLoadLog.clicked.connect(self.loadLogClicked.emit)
