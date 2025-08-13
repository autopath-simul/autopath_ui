# ui/job/jobList.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QGroupBox

class JobListPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        box = QGroupBox("----- Job List -----", self)
        v = QVBoxLayout(box)

        self.list = QListWidget()
        self.list.addItems(["Job 1: A → B", "Job 2: C → D", "Job 3: E → F", "Job 4: A → C"])
        v.addWidget(self.list)

        root = QVBoxLayout(self)
        root.addWidget(box)

    def add_item(self, text: str):
        self.list.addItem(text)
