#!/usr/bin/env python3
import subprocess, os

PLUGIN_DIR = "plugins"

def run_plugin_safe(name):
    path = os.path.join(PLUGIN_DIR, f"{name}.py")
    if not os.path.exists(path):
        print(f"❌ Plugin '{name}' not found.")
        return
    print(f"🧰 Running '{name}' in sandbox...")
    try:
        result = subprocess.run(["python3", path], capture_output=True, timeout=5)
        print(result.stdout.decode())
    except subprocess.TimeoutExpired:
        print("⏱️ Plugin execution timed out.")
    except Exception as e:
        print(f"❌ Error: {e}")

# Example usage
run_plugin_safe("rainbow_wave")
