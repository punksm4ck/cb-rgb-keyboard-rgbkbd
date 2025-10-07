# 🌈 RGB Orchestration Suite v5.3.0

A modular, multi-zone RGB control platform for Linux — built for precision, extensibility, and GUI-driven orchestration.

## 🚀 Features
- 🎨 Multi-zone RGB orchestration with GUI control
- 🔊 Audio visualizer with band-to-zone mapping
- 🧠 Real-time effect engine with ripple, pulse, and custom presets
- 🧪 Developer tools: visual debugging, tagging, and layered scheduling
- 🌐 MQTT/WebSocket sync for collaborative control
- 🧰 Modular plugin architecture with secure profiles
- 📦 Clean installer with dependency automation

## 🛠️ Installation
1. Download and extract the archive:
   ```bash
   curl -L -o rgb-orchestration-v5.3.0.tar.gz https://github.com/punksm4ck/cb-rgb-keyboard-rgbkbd/releases/download/v5.3.0/rgb-orchestration-v5.3.0.tar.gz
   tar -xzvf rgb-orchestration-v5.3.0.tar.gz
   cd rgb_release
   ```

2. Install dependencies:
   ```bash
   bash install_rgb_dependencies.sh
   ```

3. Launch the app:
   ```bash
   rgbgui
   ```

## 🖥️ Add to App Menu
To add RGB Orchestration to your system menu:
   ```bash
   cp rgb-orchestration.desktop ~/.local/share/applications/
   ```

## 📣 Contribute
Pull requests welcome! For major changes, open an issue first.

## 📜 License
MIT License. See `LICENSE` file for details.
