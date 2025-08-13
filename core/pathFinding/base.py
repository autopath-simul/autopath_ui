# core/pathFinding/base.py
from abc import ABC, abstractmethod
from typing import List
from core.graphModel import GraphModel

class PathFinder(ABC):
    """경로 탐색기 인터페이스"""
    def __init__(self, graph: GraphModel):
        self.graph = graph

    @abstractmethod
    def shortest_path(self, src: str, dst: str) -> List[str]:
        ...