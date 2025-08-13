# ui/results/distancePanel.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QGroupBox

class DistancePanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        box = QGroupBox("AGV 이동거리", self)
        v = QVBoxLayout(box)

        self.list = QListWidget()
        self.list.addItems(["AGV 1: 234.5m", "AGV 2: 201.2m", "AGV 3: 165.1m"])
        v.addWidget(self.list)

        self.btnMore = QPushButton("더보기")
        v.addWidget(self.btnMore)

        root = QVBoxLayout(self)
        root.addWidget(box)

    def set_data(self, items):
        self.list.clear()
        self.list.addItems(items)
