#!/usr/bin/env python3
import json, time, os

TELEMETRY_FILE = "telemetry.json"

def log_event(event):
    if not os.path.exists(TELEMETRY_FILE):
        with open(TELEMETRY_FILE, "w") as f:
            json.dump([], f)
    with open(TELEMETRY_FILE, "r+") as f:
        data = json.load(f)
        data.append({"event": event, "timestamp": time.time()})
        f.seek(0)
        json.dump(data, f, indent=2)
        f.truncate()

def show_dashboard():
    with open(TELEMETRY_FILE) as f:
        data = json.load(f)
        print("📊 Telemetry Dashboard")
        for entry in data[-10:]:
            print(f"{time.ctime(entry['timestamp'])}: {entry['event']}")

# Example usage
log_event("RGB GUI launched")
show_dashboard()
