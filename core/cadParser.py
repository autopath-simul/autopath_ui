# # core/cadParser.py
# from typing import Optional
# from core.graphModel import GraphModel

# class CadParser:
#     """DXF → GraphModel 변환 진입점 (지금은 데모용 더미)"""
#     def parse_dxf(self, path: str) -> Optional[GraphModel]:
#         print(f"[CadParser] DXF 파싱(stub): {path}")
#         g = GraphModel()
#         # 데모용 더미 그래프
#         g.add_node("A"); g.add_node("B"); g.add_node("C")
#         g.add_edge("A", "B", 10.0)
#         g.add_edge("B", "C", 15.0)
#         return g
# core/cadParser.py
from typing import Optional
from core.graphModel import GraphModel

class CadParser:
    """DXF → GraphModel 변환 진입점 (지금은 데모용 더미 좌표/엣지 생성)"""
    def parse_dxf(self, path: str) -> Optional[GraphModel]:
        # 실제 구현은 ezdxf 등을 붙이면 됨. 지금은 경로 출력 + 더미 그래프 반환.
        print(f"[CadParser] DXF 파싱(stub): {path}")

        g = GraphModel()
        # 더미 노드(좌표 단위: px). 적당히 삼각형 배치
        g.add_node("A", 50, 200)
        g.add_node("B", 300, 200)
        g.add_node("C", 180, 60)

        # 더미 엣지(가중치=거리 비슷하게)
        g.add_edge("A", "B", 250.0)
        g.add_edge("B", "C", 180.0)
        g.add_edge("A", "C", 180.0)

        return g
