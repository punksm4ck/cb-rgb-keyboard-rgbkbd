#!/usr/bin/env python3
import speech_recognition as sr
import subprocess

def listen_for_command():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    print("🎙️ Listening for voice command...")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"🗣️ Heard: {command}")
        if "launch rgb" in command:
            subprocess.run(["./rgbgui"])
        elif "install plugin" in command:
            plugin = command.split("install plugin")[-1].strip()
            subprocess.run(["python3", "plugin_marketplace.py", plugin])
        else:
            print("🤷 Command not recognized.")
    except sr.UnknownValueError:
        print("❌ Could not understand audio.")
    except sr.RequestError as e:
        print(f"❌ API error: {e}")

listen_for_command()
