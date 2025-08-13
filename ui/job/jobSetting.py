# ui/job/jobSetting.py
from PyQt5.QtWidgets import QWidget, QGroupBox, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QSpinBox, QPushButton
from PyQt5.QtCore import pyqtSignal

class JobSettingPanel(QWidget):
    okClicked = pyqtSignal(str, str, int)  # from, to, agv_count

    def __init__(self, parent=None):
        super().__init__(parent)

        box = QGroupBox("----- Job setting -----", self)
        v = QVBoxLayout(box)

        # From / To
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("From Node:"))
        self.cmbFrom = QComboBox(); self.cmbFrom.addItems(["자동 표시", "A", "B", "C", "D", "E", "F"])
        row1.addWidget(self.cmbFrom)
        v.addLayout(row1)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("To Node:"))
        self.cmbTo = QComboBox(); self.cmbTo.addItems(["자동 표시", "A", "B", "C", "D", "E", "F"])
        row2.addWidget(self.cmbTo)
        v.addLayout(row2)

        row3 = QHBoxLayout()
        row3.addWidget(QLabel("AGV 수량:"))
        self.spnAgv = QSpinBox(); self.spnAgv.setRange(1, 99); self.spnAgv.setValue(5)
        row3.addWidget(self.spnAgv)
        v.addLayout(row3)

        self.btnOk = QPushButton("ok")
        v.addWidget(self.btnOk)

        root = QVBoxLayout(self)
        root.addWidget(box)

        self.btnOk.clicked.connect(self._emit_ok)

    def _emit_ok(self):
        self.okClicked.emit(self.cmbFrom.currentText(), self.cmbTo.currentText(), int(self.spnAgv.value()))
