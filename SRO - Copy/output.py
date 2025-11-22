import json
from typing import List
from tasks import ScheduledBlock

def print_schedule(blocks: List[ScheduledBlock]) -> None:
    blocks_sorted = sorted(blocks, key=lambda b: (b.date.toordinal(), b.start))
    print("Schedule")
    for b in blocks_sorted:
        print(f"{b.date.isoformat()} {b.start.strftime('%H:%M')}-{b.end.strftime('%H:%M')} | {b.task_name} | {b.minutes} min")

def save_schedule_json(path: str, blocks: List[ScheduledBlock]) -> None:
    payload = []
    for b in blocks:
        payload.append({
            "task_name": b.task_name,
            "date": b.date.isoformat(),
            "start": b.start.strftime("%H:%M"),
            "end": b.end.strftime("%H:%M"),
            "minutes": b.minutes,
            "segment_index": b.segment_index,
        })
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

def save_schedule_txt(path: str, blocks: List[ScheduledBlock]) -> None:
    blocks_sorted = sorted(blocks, key=lambda b: (b.date.toordinal(), b.start))
    lines = []
    lines.append("Schedule")
    for b in blocks_sorted:
        lines.append(f"{b.date.isoformat()} {b.start.strftime('%H:%M')}-{b.end.strftime('%H:%M')} | {b.task_name} | {b.minutes} min")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
