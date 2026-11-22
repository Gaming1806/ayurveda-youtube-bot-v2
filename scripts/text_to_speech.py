#!/usr/bin/env python3
"""
Offline text-to-speech. No API key required.

Order of preference:
  1. espeak-ng command line (reliable on Linux / GitHub Actions)
  2. pyttsx3 (Windows SAPI5 / macOS NSSpeech) for local runs
"""
import argparse
import os
import shutil
import subprocess
import sys


def speak_with_espeak(text_path, output):
    cmd = ["espeak-ng", "-s", "150", "-w", output, "-f", text_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ espeak-ng failed:")
        print(result.stderr)
        sys.exit(1)
    print("✅ Using TTS driver: espeak-ng")


def speak_with_pyttsx3(text, output):
    try:
        import pyttsx3
    except ImportError:
        print("❌ Neither espeak-ng nor pyttsx3 is available.")
        print("   Linux: sudo apt install espeak-ng   |   Others: pip install pyttsx3")
        sys.exit(1)
    try:
        engine = pyttsx3.init()
    except Exception as e:
        print(f"❌ pyttsx3 could not start: {e}")
        sys.exit(1)
    engine.setProperty("rate", 150)
    engine.save_to_file(text, output)
    engine.runAndWait()
    print("✅ Using TTS driver: pyttsx3")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="content/script.txt", help="Path to script text file")
    parser.add_argument("--output", default="voice.wav", help="Output WAV file path")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"❌ Script file not found: {args.input}")
        sys.exit(1)

    with open(args.input, "r", encoding="utf-8") as f:
        text = f.read().strip()
    if not text:
        print("❌ Script text is empty.")
        sys.exit(1)

    if os.path.exists(args.output):
        os.remove(args.output)

    if shutil.which("espeak-ng"):
        speak_with_espeak(args.input, args.output)
    else:
        speak_with_pyttsx3(text, args.output)

    # An empty/header-only WAV is ~44 bytes; treat tiny files as failure
    if not os.path.exists(args.output) or os.path.getsize(args.output) < 1000:
        print("❌ Failed to create a valid voice file.")
        sys.exit(1)

    print(f"✅ Voice-over saved to {args.output}")


if __name__ == "__main__":
    main()
