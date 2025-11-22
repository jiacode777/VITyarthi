import argparse
from input_handler import load_input
from scheduler import generate_schedule
from output import print_schedule, save_schedule_json, save_schedule_txt

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--strategy", choices=["edf_priority", "priority_deadline", "shortest_first"], default="edf_priority")
    p.add_argument("--json_out")
    p.add_argument("--txt_out")
    args = p.parse_args()
    tasks, slots = load_input(args.input)
    blocks, unscheduled = generate_schedule(tasks, slots, strategy=args.strategy)
    print_schedule(blocks)
    if unscheduled:
        print("Unscheduled")
        for t in unscheduled:
            print(f"{t.name} | remaining {t.remaining_minutes} min | deadline {t.deadline.isoformat()} | priority {t.priority}")
    if args.json_out:
        save_schedule_json(args.json_out, blocks)
    if args.txt_out:
        save_schedule_txt(args.txt_out, blocks)

if __name__ == "__main__":
    main()
