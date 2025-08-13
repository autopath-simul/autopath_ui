# ui/report/reportBar.py
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QGroupBox
from PyQt5.QtCore import pyqtSignal

class ReportBar(QWidget):
    saveLogClicked = pyqtSignal()
    resultReportClicked = pyqtSignal()
    visualizeReportClicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        box = QGroupBox("", self)
        h = QHBoxLayout(box)
        h.setContentsMargins(6, 6, 6, 6)

        self.btnSaveLog = QPushButton("로그 저장")
        self.btnResultReport = QPushButton("결과 리포트")
        self.btnVizReport = QPushButton("통계 리포트 시각화")

        h.addWidget(self.btnSaveLog)
        h.addWidget(self.btnResultReport)
        h.addWidget(self.btnVizReport)
        h.addStretch(1)

        root = QHBoxLayout(self)
        root.addWidget(box)

        self.btnSaveLog.clicked.connect(self.saveLogClicked.emit)
        self.btnResultReport.clicked.connect(self.resultReportClicked.emit)
        self.btnVizReport.clicked.connect(self.visualizeReportClicked.emit)
