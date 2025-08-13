# core/agv.py
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional

class AGVState(str, Enum):
    IDLE = "idle"
    RUNNING = "running"
    WAITING = "waiting"
    DONE = "done"

@dataclass
class AGV:
    agv_id: int
    state: AGVState = AGVState.IDLE
    node: Optional[str] = None  # 현재 노드 (옵션)

class AGVFleet:
    def __init__(self, size: int = 0):
        self.agvs: List[AGV] = [AGV(i + 1) for i in range(size)]

    def acquire_idle(self) -> Optional[AGV]:
        for agv in self.agvs:
            if agv.state == AGVState.IDLE:
                return agv
        return None

    def list(self) -> List[AGV]:
        return list(self.agvs)