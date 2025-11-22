from datetime import datetime, timedelta, date
from typing import List, Tuple, Dict
from tasks import Task, TimeSlot, ScheduledBlock

def _task_key(task: Task, current_date: date, strategy: str):
    overdue_flag = 0 if task.deadline < current_date else 1
    if strategy == "priority_deadline":
        return (overdue_flag, -task.priority, task.deadline.toordinal(), -task.remaining_minutes)
    if strategy == "shortest_first":
        return (overdue_flag, task.remaining_minutes, task.deadline.toordinal(), -task.priority)
    return (overdue_flag, task.deadline.toordinal(), -task.priority, -task.remaining_minutes)

def generate_schedule(tasks: List[Task], slots: List[TimeSlot], strategy: str = "edf_priority") -> Tuple[List[ScheduledBlock], List[Task]]:
    slots_sorted = sorted(slots, key=lambda s: (s.date.toordinal(), s.start))
    active = [t for t in tasks]
    segments: Dict[str, int] = {}
    blocks: List[ScheduledBlock] = []
    for slot in slots_sorted:
        remaining = slot.length_minutes()
        cursor = datetime.combine(slot.date, slot.start)
        while remaining > 0:
            candidates = [t for t in active if t.remaining_minutes > 0]
            if not candidates:
                break
            chosen = min(candidates, key=lambda t: _task_key(t, slot.date, strategy))
            allocate = min(chosen.remaining_minutes, remaining)
            seg_index = segments.get(chosen.name, 0) + 1
            segments[chosen.name] = seg_index
            end_dt = cursor + timedelta(minutes=allocate)
            block = ScheduledBlock(
                task_name=chosen.name,
                date=slot.date,
                start=cursor.time(),
                end=end_dt.time(),
                minutes=allocate,
                segment_index=seg_index,
            )
            blocks.append(block)
            chosen.remaining_minutes -= allocate
            remaining -= allocate
            cursor = end_dt
    unscheduled = [t for t in active if t.remaining_minutes > 0]
    return blocks, unscheduled
