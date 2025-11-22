import json
from datetime import date, time
from typing import List, Tuple
from tasks import Task, TimeSlot, priority_from_str

def parse_date(s: str) -> date:
    return date.fromisoformat(s)

def parse_time(s: str) -> time:
    return time.fromisoformat(s)

def load_input(path: str) -> Tuple[List[Task], List[TimeSlot]]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    tasks_raw = data.get("tasks", [])
    slots_raw = data.get("time_slots", [])
    tasks: List[Task] = []
    for t in tasks_raw:
        name = str(t["name"])
        duration = int(t["duration_minutes"])
        deadline = parse_date(str(t["deadline"]))
        priority = t["priority"]
        p = priority if isinstance(priority, int) else priority_from_str(str(priority))
        tasks.append(Task(name=name, duration_minutes=duration, deadline=deadline, priority=p))
    slots: List[TimeSlot] = []
    for s in slots_raw:
        d = parse_date(str(s["date"]))
        start = parse_time(str(s["start"]))
        end = parse_time(str(s["end"]))
        slots.append(TimeSlot(date=d, start=start, end=end))
    tasks = [t for t in tasks if t.duration_minutes > 0]
    slots = [s for s in slots if s.length_minutes() > 0]
    return tasks, slots
