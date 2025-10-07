#!/bin/bash
echo "🌈 RGB Orchestration Installer"

# Download and extract
curl -L -o rgb-orchestration-v5.3.0.tar.gz https://github.com/punksm4ck/cb-rgb-keyboard-rgbkbd/releases/download/v5.3.0/rgb-orchestration-v5.3.0.tar.gz
tar -xzvf rgb-orchestration-v5.3.0.tar.gz
cd rgb_release

# Install dependencies
bash install_rgb_dependencies.sh

# Install icon and launcher
mkdir -p ~/.local/share/icons ~/.local/share/applications
cp rgb_controller_splash.png ~/.local/share/icons/
cp rgb-orchestration.desktop ~/.local/share/applications/

echo "🚀 Launching RGB GUI..."
rgbgui
