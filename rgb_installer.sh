#!/bin/bash
echo "🌈 RGB Orchestration Installer"

echo "📦 Downloading .tar.gz installer package..."
curl -L -o rgb-orchestration-v5.3.0.tar.gz https://github.com/punksm4ck/cb-rgb-keyboard-rgbkbd/releases/download/v5.3.0/rgb-orchestration-v5.3.0.tar.gz

echo "📂 Extracting..."
tar -xzvf rgb-orchestration-v5.3.0.tar.gz
cd rgb_release

echo "🔧 Installing dependencies..."
bash install_rgb_dependencies.sh

echo "🚀 Launching RGB GUI..."
rgbgui
