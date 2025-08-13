
# ui/mainWindow.py
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QFrame,
    QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt

# ── UI 구성요소 import (파일명/클래스명은 네가 만든 구조에 맞춤) ──
from ui.bar.fileBar import FileBar
from ui.bar.playbackBar import PlaybackBar
from ui.canvas.cadCanvas import CadCanvas
from ui.job.jobSetting import JobSettingPanel
from ui.job.jobList import JobListPanel
from ui.results.resultsPanel import ResultsPanel
from ui.report.reportBar import ReportBar


class MainWindow(QMainWindow):
    """
    AutoPath Simul 메인 프레임
    - 상단: FileBar(도면/로그) + PlaybackBar(재생)
    - 중앙 좌측: CadCanvas (시뮬레이션 디스플레이)
    - 중앙 우측: JobSetting / JobList / Results / ReportBar
    """
    def __init__(self, engine=None, job_manager=None, parent=None):
        super().__init__(parent)
        self.engine = engine              # core.engine.SimulationEngine (옵션)
        self.job_manager = job_manager    # core.job.JobManager (옵션)

        self.setWindowTitle("AutoPath Simul")
        self.resize(1280, 720)  # 16:9 기본

        self._build_ui()
        self._connect_signals()

    # --------------------------
    # UI 구성
    # --------------------------
    def _build_ui(self):
        central = QWidget(self)
        self.setCentralWidget(central)

        # 상단 바(파일/재생)
        self.fileBar = FileBar(self)
        self.playbackBar = PlaybackBar(self)

        topBar = QHBoxLayout()
        topBar.addWidget(self.fileBar)
        topBar.addStretch(1)
        topBar.addWidget(self.playbackBar)

        # 좌측: 캔버스
        self.canvas = CadCanvas(self)
        self.canvas.setFrameShape(QFrame.Panel)
        self.canvas.setFrameShadow(QFrame.Sunken)
        self.canvas.setMinimumWidth(800)

        # 우측: 사이드 패널 세트
        self.jobSetting = JobSettingPanel(self)
        self.jobList = JobListPanel(self)
        self.results = ResultsPanel(self)
        self.reportBar = ReportBar(self)

        sideCol = QVBoxLayout()
        sideCol.addWidget(self.jobSetting)
        sideCol.addWidget(self.jobList, 1)   # 리스트는 확장
        sideCol.addWidget(self.results, 2)   # 결과 패널은 더 크게
        sideCol.addWidget(self.reportBar)

        # 중앙 레이아웃 (좌: 캔버스 | 우: 사이드)
        middle = QHBoxLayout()
        middle.addWidget(self.canvas, 3)
        rightWrap = QWidget(self)
        rightWrap.setLayout(sideCol)
        rightWrap.setMinimumWidth(360)
        middle.addWidget(rightWrap, 2)

        # 최상위 레이아웃
        root = QVBoxLayout(central)
        root.addLayout(topBar)
        root.addLayout(middle, 1)

        # 상태바(선택)
        self.statusBar().showMessage("Ready")

    # --------------------------
    # 시그널 연결
    # --------------------------
    def _connect_signals(self):
        # FileBar
        if hasattr(self.fileBar, "loadDxfClicked"):
            self.fileBar.loadDxfClicked.connect(self.onLoadDxf)
        if hasattr(self.fileBar, "loadLogClicked"):
            self.fileBar.loadLogClicked.connect(self.onLoadLog)

        # PlaybackBar
        if hasattr(self.playbackBar, "startClicked"):
            self.playbackBar.startClicked.connect(self.onStart)
        if hasattr(self.playbackBar, "pauseClicked"):
            self.playbackBar.pauseClicked.connect(self.onPause)
        if hasattr(self.playbackBar, "stopClicked"):
            self.playbackBar.stopClicked.connect(self.onStop)

        # JobSetting -> JobManager
        if hasattr(self.jobSetting, "okClicked"):  # (fromNode, toNode, agvCount)
            self.jobSetting.okClicked.connect(self.onJobSubmit)

        # ReportBar
        if hasattr(self.reportBar, "saveLogClicked"):
            self.reportBar.saveLogClicked.connect(self.onSaveLog)
        if hasattr(self.reportBar, "resultReportClicked"):
            self.reportBar.resultReportClicked.connect(self.onResultReport)
        if hasattr(self.reportBar, "visualizeReportClicked"):
            self.reportBar.visualizeReportClicked.connect(self.onVisualizeReport)

    # --------------------------
    # 슬롯 구현(오늘은 print만)
    # --------------------------
    def onLoadDxf(self):
        path, _ = QFileDialog.getOpenFileName(self, "도면 불러오기", "", "DXF Files (*.dxf);;All Files (*)")
        if not path:
            print("[File] DXF 선택 취소")
            return
        print(f"[File] DXF 로드: {path}")
        # 캔버스/그래프 로딩은 나중에 core.cad_parser 붙일 것
        self.statusBar().showMessage(f"Loaded DXF: {path}")

    def onLoadLog(self):
        path, _ = QFileDialog.getOpenFileName(self, "로그 불러오기", "", "CSV Files (*.csv);;All Files (*)")
        if not path:
            print("[File] 로그 선택 취소")
            return
        print(f"[File] 로그 로드: {path}")
        self.statusBar().showMessage(f"Loaded Log: {path}")

    def onSaveLog(self):
        path, _ = QFileDialog.getSaveFileName(self, "로그 저장", "simulation_log.csv", "CSV Files (*.csv)")
        if not path:
            print("[Report] 저장 취소")
            return
        print(f"[Report] 로그 저장: {path}")
        self.statusBar().showMessage(f"Saved Log: {path}")

    def onResultReport(self):
        print("[Report] 결과 리포트 생성 (stub)")
        QMessageBox.information(self, "Report", "결과 리포트 생성 (stub)")

    def onVisualizeReport(self):
        print("[Report] 통계 리포트 시각화 (stub)")
        QMessageBox.information(self, "Report", "통계 리포트 시각화 (stub)")

    def onStart(self):
        print("[Sim] Start")
        if self.engine and hasattr(self.engine, "start"):
            self.engine.start()
        self.statusBar().showMessage("Running")

    def onPause(self):
        print("[Sim] Pause")
        if self.engine and hasattr(self.engine, "pause"):
            self.engine.pause()
        self.statusBar().showMessage("Paused")

    def onStop(self):
        print("[Sim] Stop")
        if self.engine and hasattr(self.engine, "stop"):
            self.engine.stop()
        self.statusBar().showMessage("Stopped")

    def onJobSubmit(self, from_node: str, to_node: str, agv_count: int):
        print(f"[Job] Submit: {from_node} -> {to_node} (AGV {agv_count})")
        # JobManager가 있으면 전달
        if self.job_manager and hasattr(self.job_manager, "submit_job"):
            self.job_manager.submit_job(from_node, to_node, agv_count)
        # JobListPanel에 표시(해당 패널에 add_item(str) 같은 메서드 만들어 두면 좋음)
        if hasattr(self.jobList, "add_item"):
            self.jobList.add_item(f"{from_node} → {to_node} (x{agv_count})")

    # 선택: 외부에서 엔진/매니저 주입
    def bindEngine(self, engine):
        self.engine = engine

    def bindJobManager(self, job_manager):
        self.job_manager = job_manager
