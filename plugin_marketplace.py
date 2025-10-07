#!/usr/bin/env python3
import os
import json

PLUGIN_DIR = "plugins"
MARKETPLACE_FILE = "marketplace.json"

def load_marketplace():
    if not os.path.exists(MARKETPLACE_FILE):
        print("⚠️ No marketplace.json found.")
        return []
    with open(MARKETPLACE_FILE) as f:
        return json.load(f)

def list_available_plugins():
    print("🛒 Available plugins:")
    for plugin in load_marketplace():
        print(f" - {plugin['name']}: {plugin['description']}")

def install_plugin(name):
    plugin = next((p for p in load_marketplace() if p['name'] == name), None)
    if plugin:
        print(f"📦 Installing {name}...")
        os.system(f"curl -L -o plugins/{name}.py {plugin['url']}")
    else:
        print(f"❌ Plugin '{name}' not found.")

# Example usage
list_available_plugins()
