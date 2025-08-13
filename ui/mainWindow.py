# ui/mainWindow.py
from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QFrame,
    QFileDialog, QMessageBox
)

# ── UI 컴포넌트 ────────────────────────────────────────────────────────────────
from ui.bar.fileBar import FileBar
from ui.bar.playbackBar import PlaybackBar
from ui.canvas.cadCanvas import CadCanvas
from ui.job.jobSetting import JobSettingPanel
from ui.job.jobList import JobListPanel
from ui.results.resultsPanel import ResultsPanel
from ui.report.reportBar import ReportBar

# ── Core (DXF → GraphModel, 엔진/잡매니저는 주입받아 사용) ───────────────────
from core.cadParser import CadParser
from core.graphModel import GraphModel


class MainWindow(QMainWindow):
    """
    AutoPath Simul 메인 프레임
      - 상단: FileBar(도면/로그) + PlaybackBar(▶⏸⏹)
      - 중앙: 좌측 CadCanvas, 우측 Job/Results/Report 패널
    버튼은 print/MessageBox만 연결된 시연용 스텁.
    """

    def __init__(self, engine=None, job_manager=None, parent: Optional[QWidget] = None):
        super().__init__(parent)

        # 주입(없어도 실행 가능)
        self.engine = engine
        self.job_manager = job_manager

        # 파서/그래프
        self.parser = CadParser()
        self.graph: Optional[GraphModel] = None

        # 윈도 기본 설정
        self.setWindowTitle("AutoPath Simul")
        self.resize(1280, 720)  # 16:9

        # UI 구성 & 시그널 연결
        self._build_ui()
        self._connect_signals()

        # 상태바
        self.statusBar().showMessage("Ready")

    # ──────────────────────────────────────────────────────────────────────────
    # UI 구성
    # ──────────────────────────────────────────────────────────────────────────
    def _build_ui(self) -> None:
        central = QWidget(self)
        self.setCentralWidget(central)

        # 상단 바: 파일 + 재생
        self.fileBar = FileBar(self)
        self.playbackBar = PlaybackBar(self)

        topBar = QHBoxLayout()
        topBar.setContentsMargins(6, 6, 6, 6)
        topBar.addWidget(self.fileBar)
        topBar.addStretch(1)
        topBar.addWidget(self.playbackBar)

        # 좌측 캔버스
        self.canvas = CadCanvas(self)
        self.canvas.setFrameShape(QFrame.Panel)
        self.canvas.setFrameShadow(QFrame.Sunken)
        self.canvas.setMinimumWidth(800)

        # 우측 사이드 패널
        self.jobSetting = JobSettingPanel(self)
        self.jobList = JobListPanel(self)
        self.results = ResultsPanel(self)
        self.reportBar = ReportBar(self)

        sideCol = QVBoxLayout()
        sideCol.setContentsMargins(6, 6, 6, 6)
        sideCol.setSpacing(8)
        sideCol.addWidget(self.jobSetting)
        sideCol.addWidget(self.jobList, 1)   # 리스트는 늘어나게
        sideCol.addWidget(self.results, 2)   # 결과는 더 크게
        sideCol.addWidget(self.reportBar)

        rightWrap = QWidget(self)
        rightWrap.setLayout(sideCol)
        rightWrap.setMinimumWidth(360)

        # 중앙(좌/우)
        middle = QHBoxLayout()
        middle.setContentsMargins(6, 0, 6, 6)
        middle.setSpacing(12)
        middle.addWidget(self.canvas, 3)
        middle.addWidget(rightWrap, 2)

        # 최상위 레이아웃
        root = QVBoxLayout(central)
        root.setContentsMargins(6, 6, 6, 6)
        root.setSpacing(8)
        root.addLayout(topBar)
        root.addLayout(middle, 1)

    # ──────────────────────────────────────────────────────────────────────────
    # 시그널 연결
    # ──────────────────────────────────────────────────────────────────────────
    def _connect_signals(self) -> None:
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

        # JobSetting(ok → JobManager 전달 + JobList 표시)
        if hasattr(self.jobSetting, "okClicked"):
            self.jobSetting.okClicked.connect(self.onJobSubmit)

        # ReportBar
        if hasattr(self.reportBar, "saveLogClicked"):
            self.reportBar.saveLogClicked.connect(self.onSaveLog)
        if hasattr(self.reportBar, "resultReportClicked"):
            self.reportBar.resultReportClicked.connect(self.onResultReport)
        if hasattr(self.reportBar, "visualizeReportClicked"):
            self.reportBar.visualizeReportClicked.connect(self.onVisualizeReport)

    # ──────────────────────────────────────────────────────────────────────────
    # 슬롯 (시연용: print/MessageBox/상태바만)
    # ──────────────────────────────────────────────────────────────────────────
    def onLoadDxf(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "도면 불러오기", "", "DXF Files (*.dxf);;All Files (*)"
        )
        if not path:
            print("[File] DXF 선택 취소")
            return

        print(f"[File] DXF 로드: {path}")
        try:
            g = self.parser.parse_dxf(path)  # GraphModel (더미)
            if not g or not getattr(g, "pos", None):
                QMessageBox.warning(self, "DXF", "그래프 생성 실패(더미).")
                return
            self.graph = g
            self.canvas.render_graph(self.graph)  # ← 좌표/엣지 간단 렌더
            self.statusBar().showMessage(f"Loaded DXF (dummy render): {path}")
        except Exception as e:
            print("[File] DXF 파싱 에러:", e)
            QMessageBox.critical(self, "DXF", f"파싱 중 오류 발생:\n{e}")

    def onLoadLog(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "로그 불러오기", "", "CSV Files (*.csv);;All Files (*)"
        )
        if not path:
            print("[File] 로그 선택 취소")
            return
        print(f"[File] 로그 로드: {path}")
        self.statusBar().showMessage(f"Loaded Log: {path}")

    def onSaveLog(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self, "로그 저장", "simulation_log.csv", "CSV Files (*.csv)"
        )
        if not path:
            print("[Report] 저장 취소")
            return
        print(f"[Report] 로그 저장: {path}")
        self.statusBar().showMessage(f"Saved Log: {path}")

    def onResultReport(self) -> None:
        print("[Report] 결과 리포트 생성 (stub)")
        QMessageBox.information(self, "Report", "결과 리포트 생성 (stub)")

    def onVisualizeReport(self) -> None:
        print("[Report] 통계 리포트 시각화 (stub)")
        QMessageBox.information(self, "Report", "통계 리포트 시각화 (stub)")

    def onStart(self) -> None:
        print("[Sim] Start")
        if self.engine and hasattr(self.engine, "start"):
            self.engine.start()
        self.statusBar().showMessage("Running")

    def onPause(self) -> None:
        print("[Sim] Pause")
        if self.engine and hasattr(self.engine, "pause"):
            self.engine.pause()
        self.statusBar().showMessage("Paused")

    def onStop(self) -> None:
        print("[Sim] Stop")
        if self.engine and hasattr(self.engine, "stop"):
            self.engine.stop()
        self.statusBar().showMessage("Stopped")

    def onJobSubmit(self, from_node: str, to_node: str, agv_count: int) -> None:
        print(f"[Job] Submit: {from_node} → {to_node} (AGV {agv_count})")

        # Core에 전달
        if self.job_manager and hasattr(self.job_manager, "submit_job"):
            self.job_manager.submit_job(from_node, to_node, agv_count)

        # 리스트 패널 반영
        if hasattr(self.jobList, "add_item"):
            self.jobList.add_item(f"{from_node} → {to_node} (x{agv_count})")

    # 외부에서 엔진/매니저 바인딩하고 싶을 때
    def bindEngine(self, engine) -> None:
        self.engine = engine

    def bindJobManager(self, job_manager) -> None:
        self.job_manager = job_manager
