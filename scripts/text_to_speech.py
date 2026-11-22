#!/usr/bin/env python3
"""
Offline text-to-speech using pyttsx3.
Saves voice.wav in the project root. No API key required.
"""
import argparse
import os
import sys

try:
    import pyttsx3
except ImportError:
    print("❌ pyttsx3 is not installed. Run: pip install pyttsx3")
    sys.exit(1)


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

    engine = pyttsx3.init()
    # Slightly slower rate for clarity
    engine.setProperty("rate", 150)
    engine.save_to_file(text, args.output)
    engine.runAndWait()

    if not os.path.exists(args.output):
        print("❌ Failed to create voice file.")
        sys.exit(1)

    print(f"✅ Voice-over saved to {args.output}")


if __name__ == "__main__":
    main()