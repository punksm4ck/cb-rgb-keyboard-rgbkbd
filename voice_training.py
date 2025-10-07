#!/usr/bin/env python3
import json

TRAINING_FILE = "voice_commands.json"

def add_command(phrase, action):
    with open(TRAINING_FILE, "r+") as f:
        data = json.load(f)
        data[phrase] = action
        f.seek(0)
        json.dump(data, f, indent=2)
        f.truncate()
    print(f"✅ Trained: '{phrase}' → {action}")

def list_commands():
    with open(TRAINING_FILE) as f:
        data = json.load(f)
        for phrase, action in data.items():
            print(f"🗣️ '{phrase}' → {action}")

# Initialize file if missing
try:
    with open(TRAINING_FILE) as f:
        pass
except FileNotFoundError:
    with open(TRAINING_FILE, "w") as f:
        json.dump({}, f)

# Example usage
add_command("launch rgb", "./rgbgui")
add_command("install rainbow", "python3 plugin_marketplace.py rainbow_wave")
list_commands()
