from dataclasses import dataclass, field
from datetime import date, time, datetime
from typing import Optional

PRIORITY_MAP = {"low": 1, "medium": 2, "high": 3}

def priority_from_str(s: str) -> int:
    return PRIORITY_MAP.get(s.strip().lower(), 1)

@dataclass
class Task:
    name: str
    duration_minutes: int
    deadline: date
    priority: int
    remaining_minutes: int = field(init=False)

    def __post_init__(self):
        self.remaining_minutes = self.duration_minutes

@dataclass
class TimeSlot:
    date: date
    start: time
    end: time

    def length_minutes(self) -> int:
        dt_start = datetime.combine(self.date, self.start)
        dt_end = datetime.combine(self.date, self.end)
        return max(0, int((dt_end - dt_start).total_seconds() // 60))

@dataclass
class ScheduledBlock:
    task_name: str
    date: date
    start: time
    end: time
    minutes: int
    segment_index: int
