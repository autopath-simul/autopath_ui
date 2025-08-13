# core/pathFinding/dijkstra.py
from typing import Dict, List, Tuple
import heapq
from core.graphModel import GraphModel
from core.pathFinding.base import PathFinder

class DijkstraPathFinder(PathFinder):
    """힙 기반 다익스트라 구현"""
    def shortest_path(self, src: str, dst: str) -> List[str]:
        if src not in self.graph.nodes or dst not in self.graph.nodes:
            print("[Dijkstra] 존재하지 않는 노드")
            return []

        dist: Dict[str, float] = {n: float("inf") for n in self.graph.nodes}
        prev: Dict[str, str] = {}
        dist[src] = 0.0
        pq: List[Tuple[float, str]] = [(0.0, src)]

        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
            if u == dst:
                break
            for v in self.graph.neighbors(u):
                nd = d + self.graph.weight(u, v)
                if nd < dist[v]:
                    dist[v] = nd
                    prev[v] = u
                    heapq.heappush(pq, (nd, v))

        if src == dst:
            return [src]
        if dst not in prev:
            print("[Dijkstra] 경로 없음")
            return []

        # 경로 복원
        path = [dst]
        while path[-1] != src:
            path.append(prev[path[-1]])
        path.reverse()
        print(f"[Dijkstra] {src} → {dst} 경로: {path} (거리 {dist[dst]:.2f})")
        return path