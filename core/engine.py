# core/engine.py
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

class SimulationEngine(QObject):
    """시뮬레이션 상태를 관리하는 가장 얇은 엔진 스텁"""
    statsUpdated = pyqtSignal(dict)      # {"avg_time": "00:00:00", ...}
    stateChanged = pyqtSignal(str)       # "running" | "paused" | "stopped"

    def __init__(self, parent=None):
        super().__init__(parent)
        self._running = False

    @pyqtSlot()
    def start(self):
        self._running = True
        print("[Engine] start()")
        self.stateChanged.emit("running")

    @pyqtSlot()
    def pause(self):
        if not self._running:
            print("[Engine] pause() ignored (not running)")
            return
        self._running = False
        print("[Engine] pause()")
        self.stateChanged.emit("paused")

    @pyqtSlot()
    def stop(self):
        self._running = False
        print("[Engine] stop()")
        self.stateChanged.emit("stopped")
