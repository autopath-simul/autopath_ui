# ui/canvas/cadCanvas.py
from PyQt5.QtWidgets import (
    QGraphicsView, QGraphicsScene,
    QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsTextItem
)
from PyQt5.QtGui import QPen, QPainter
from PyQt5.QtCore import Qt, QRectF
from core.graphModel import GraphModel

class CadCanvas(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        # ❌ self.setRenderHint(self.renderHints() | 0x01)
        # ✅ 단일 플래그로 설정
        self.setRenderHint(QPainter.Antialiasing, True)
        # 또는: self.setRenderHints(self.renderHints() | QPainter.Antialiasing)

        self._add_placeholder()

    def _add_placeholder(self):
        hint = QGraphicsTextItem("1) CAD 도면 표시\n2) 노드 클릭 → From/To 설정\n3) AGV 아이콘 이동(향후)")
        hint.setDefaultTextColor(Qt.darkGray)
        self.scene.addItem(hint)

    def clearCanvas(self):
        self.scene.clear()

    def render_graph(self, g: GraphModel):
        """GraphModel의 pos/edge를 간단히 그려준다."""
        self.scene.clear()

        # 엣지 먼저
        pen_edge = QPen(Qt.darkGray)
        pen_edge.setWidth(2)
        for u, nbrs in g.adj.items():
            for v in nbrs.keys():
                if u > v:  # 무방향 중복 방지
                    continue
                if u not in g.pos or v not in g.pos:
                    continue
                x1, y1 = g.pos[u]
                x2, y2 = g.pos[v]
                line = QGraphicsLineItem(x1, y1, x2, y2)
                line.setPen(pen_edge)
                self.scene.addItem(line)

        # 노드(원형 + 라벨)
        pen_node = QPen(Qt.black)
        pen_node.setWidth(1)
        radius = 8
        for node_id, (x, y) in g.pos.items():
            dot = QGraphicsEllipseItem(QRectF(x - radius, y - radius, radius * 2, radius * 2))
            dot.setPen(pen_node)
            dot.setBrush(Qt.white)
            self.scene.addItem(dot)

            label = QGraphicsTextItem(node_id)
            label.setDefaultTextColor(Qt.black)
            label.setPos(x + 6, y - 18)
            self.scene.addItem(label)

        # 보기 좋게 맞추기
        self.scene.setSceneRect(self.scene.itemsBoundingRect().adjusted(-40, -40, 40, 40))
        self.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)