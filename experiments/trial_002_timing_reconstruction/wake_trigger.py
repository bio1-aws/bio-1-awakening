import json
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta

STATE_FILE = r"c:\bio-1-awakening\experiments\trial_002_timing_reconstruction\state.json"
LOG_FILE = r"c:\bio-1-awakening\experiments\trial_002_timing_reconstruction\wake_log.txt"

def log(msg):
    timestamp = datetime.now().isoformat()
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {msg}\n")

def main():
    log("WAKE TRIGGER ACTIVATED")
    
    if not os.path.exists(STATE_FILE):
        log("ERROR: State file not found")
        return
    
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        state = json.load(f)
    
    state["wake_count"] = state.get("wake_count", 0) + 1
    state["last_wake_time"] = datetime.now().isoformat()
    
    # Process next task
    if state.get("task_queue"):
        next_task = state["task_queue"].pop(0)
        state["completed_tasks"].append(next_task)
        log(f"Executing task: {next_task}")
        state["current_phase"] = f"completed_{next_task}"
    
    # Schedule next wake
    state["next_wake_time"] = (datetime.now() + timedelta(minutes=1)).isoformat()
    
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
    
    log(f"Wake #{state['wake_count']} complete. Next: {state['next_wake_time']}")
    log(f"Remaining tasks: {state['task_queue']}")

if __name__ == "__main__":
    main()
