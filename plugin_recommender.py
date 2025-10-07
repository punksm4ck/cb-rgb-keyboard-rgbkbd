#!/usr/bin/env python3
import json, random

def recommend_plugins():
    with open("telemetry.json") as f:
        events = json.load(f)
    keywords = [e["event"] for e in events if "plugin" in e["event"]]
    suggestions = {
        "audio": "audio_sync",
        "rainbow": "rainbow_wave",
        "debug": "visual_debugger"
    }
    print("🧠 Recommended Plugins:")
    for k, v in suggestions.items():
        if any(k in e for e in keywords):
            print(f" - {v} (based on usage of '{k}')")
    if not keywords:
        print(" - rainbow_wave (default suggestion)")

recommend_plugins()
