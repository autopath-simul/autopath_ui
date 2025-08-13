# ui/results/bottleneckPanel.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QGroupBox

class BottleneckPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        box = QGroupBox("병목 구간 통계", self)
        v = QVBoxLayout(box)

        self.list = QListWidget()
        self.list.addItems(["A → B: 12초", "C → D: 8초", "E → F: 5초"])
        v.addWidget(self.list)

        self.btnMore = QPushButton("더보기")
        v.addWidget(self.btnMore)

        root = QVBoxLayout(self)
        root.addWidget(box)

    def set_data(self, items):
        self.list.clear()
        self.list.addItems(items)
