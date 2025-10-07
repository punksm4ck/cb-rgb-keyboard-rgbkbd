#!/bin/bash
echo "🔧 Installing RGB orchestration dependencies..."
sudo apt update
sudo apt install -y python3-pip python3-tk libportaudio2 libpulse-dev libasound2-dev ffmpeg sox pavucontrol
pip3 install --user numpy sounddevice requests paho-mqtt imageio pillow matplotlib pygments flask
echo "✅ Dependencies installed."
