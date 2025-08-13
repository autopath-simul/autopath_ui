# ui/bar/playbackBar.py
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt5.QtCore import pyqtSignal

class PlaybackBar(QWidget):
    startClicked = pyqtSignal()
    pauseClicked = pyqtSignal()
    stopClicked  = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.btnStart = QPushButton("▶ 시작")
        self.btnPause = QPushButton("⏸ 일시정지")
        self.btnStop  = QPushButton("⏹ 정지")

        layout.addWidget(self.btnStart)
        layout.addWidget(self.btnPause)
        layout.addWidget(self.btnStop)

        self.btnStart.clicked.connect(self.startClicked.emit)
        self.btnPause.clicked.connect(self.pauseClicked.emit)
        self.btnStop.clicked.connect(self.stopClicked.emit)
