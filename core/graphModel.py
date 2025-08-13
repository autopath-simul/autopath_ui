# # core/graphModel.py
# from dataclasses import dataclass
# from typing import Dict, List

# @dataclass(frozen=True)
# class Node:
#     id: str

# class GraphModel:
#     """무방향 가중 그래프 (최소 스텁)"""
#     def __init__(self):
#         self.nodes: Dict[str, Node] = {}
#         self.adj: Dict[str, Dict[str, float]] = {}  # u -> {v: weight}

#     def add_node(self, node_id: str) -> str:
#         if node_id not in self.nodes:
#             self.nodes[node_id] = Node(node_id)
#             self.adj.setdefault(node_id, {})
#         return node_id

#     def add_edge(self, u: str, v: str, w: float):
#         self.add_node(u); self.add_node(v)
#         self.adj[u][v] = float(w)
#         self.adj[v][u] = float(w)  # 기본: 무방향

#     def neighbors(self, u: str) -> List[str]:
#         return list(self.adj.get(u, {}).keys())

#     def weight(self, u: str, v: str) -> float:
#         return float(self.adj.get(u, {}).get(v, float("inf")))



# core/graphModel.py
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional

@dataclass(frozen=True)
class Node:
    id: str

class GraphModel:
    """무방향 가중 그래프 (+ 2D 좌표)"""
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.adj: Dict[str, Dict[str, float]] = {}      # u -> {v: weight}
        self.pos: Dict[str, Tuple[float, float]] = {}   # node_id -> (x, y)

    def add_node(self, node_id: str, x: Optional[float] = None, y: Optional[float] = None) -> str:
        if node_id not in self.nodes:
            self.nodes[node_id] = Node(node_id)
            self.adj.setdefault(node_id, {})
        if x is not None and y is not None:
            self.pos[node_id] = (float(x), float(y))
        return node_id

    def set_pos(self, node_id: str, x: float, y: float) -> None:
        self.add_node(node_id)
        self.pos[node_id] = (float(x), float(y))

    def add_edge(self, u: str, v: str, w: float):
        self.add_node(u); self.add_node(v)
        self.adj[u][v] = float(w)
        self.adj[v][u] = float(w)  # 기본: 무방향

    def neighbors(self, u: str) -> List[str]:
        return list(self.adj.get(u, {}).keys())

    def weight(self, u: str, v: str) -> float:
        return float(self.adj.get(u, {}).get(v, float("inf")))
