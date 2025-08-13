# ui/canvas/cadCanvas.py
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsTextItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter


class CadCanvas(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        # self.setRenderHint(self.renderHints() | 0x01)  # Antialiasing
        self.setRenderHint(QPainter.Antialiasing, True)
        self._add_placeholder()

    def _add_placeholder(self):
        hint = QGraphicsTextItem("1) CAD 도면 표시\n2) 노드 클릭 → From, To 설정\n3) AGV 아이콘 이동(향후)")
        hint.setDefaultTextColor(Qt.darkGray)
        self.scene.addItem(hint)

    # 나중에 DXF 렌더링 붙일 자리
    def clearCanvas(self):
        self.scene.clear()
        self._add_placeholder()
