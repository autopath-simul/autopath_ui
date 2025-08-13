# ui/results/resultsPanel.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox, QHBoxLayout
from ui.results.bottleneckPanel import BottleneckPanel
from ui.results.distancePanel import DistancePanel

class ResultsPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 상단 요약
        summaryBox = QGroupBox("----- Results -----", self)
        sv = QVBoxLayout(summaryBox)
        self.lblSummary = QLabel("현재 AGV 수량: 5대\n진행상태: 진행중\n평균 이동 시간: 00:00:00")
        sv.addWidget(self.lblSummary)

        # 하단 두 패널
        self.bottleneck = BottleneckPanel(self)
        self.distance = DistancePanel(self)

        twoCol = QHBoxLayout()
        twoCol.addWidget(self.bottleneck)
        twoCol.addWidget(self.distance)

        root = QVBoxLayout(self)
        root.addWidget(summaryBox)
        root.addLayout(twoCol)

    def update(self, stats=None):
        # 시연용 더미 업데이트
        self.lblSummary.setText("현재 AGV 수량: 5대\n진행상태: 진행중\n평균 이동 시간: 00:00:00")
