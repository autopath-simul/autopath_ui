# core/job.py
from dataclasses import dataclass
from typing import List

@dataclass
class Job:
    src: str
    dst: str
    agv_count: int = 1

class JobManager:
    def __init__(self):
        self._jobs: List[Job] = []

    def submit_job(self, src: str, dst: str, agv_count: int = 1):
        job = Job(src, dst, agv_count)
        self._jobs.append(job)
        print(f"[JobManager] 등록: {src} → {dst} (x{agv_count})")

    def list_jobs(self) -> List[Job]:
        return list(self._jobs)