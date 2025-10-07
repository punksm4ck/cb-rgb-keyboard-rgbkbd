#!/usr/bin/env python3
import os, json, requests

PLUGIN_DIR = "plugins"
MARKETPLACE_FILE = "marketplace.json"

def load_marketplace():
    with open(MARKETPLACE_FILE) as f:
        return json.load(f)

def check_updates():
    print("🔄 Checking for plugin updates...")
    for plugin in load_marketplace():
        local_path = os.path.join(PLUGIN_DIR, f"{plugin['name']}.py")
        if os.path.exists(local_path):
            local_hash = hash(open(local_path).read())
            remote_code = requests.get(plugin['url']).text
            remote_hash = hash(remote_code)
            if local_hash != remote_hash:
                print(f"⬆️ Update available for {plugin['name']}")
            else:
                print(f"✅ {plugin['name']} is up to date")
        else:
            print(f"❌ {plugin['name']} not installed")

check_updates()
