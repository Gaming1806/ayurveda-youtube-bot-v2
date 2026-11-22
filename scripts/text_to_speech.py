#!/usr/bin/env python3
"""
Text-to-speech with natural neural voices.

Engines (--engine auto tries them in this order):
  1. edge-tts   Microsoft neural voices, free, no API key, needs internet (works on GitHub Actions)
  2. espeak-ng  robotic but fully offline (fallback)
  3. pyttsx3    Windows / macOS system voices (last resort for local runs)

List available voices:   edge-tts --list-voices
Hinglish (Devanagari Hindi + English words):  hi-IN-SwaraNeural (female, default)   hi-IN-MadhurNeural (male)
English only:            en-IN-NeerjaNeural   en-IN-PrabhatNeural   en-US-AriaNeural   en-US-GuyNeural
"""
import argparse
import asyncio
import os
import shutil
import subprocess
import sys
import tempfile

DEFAULT_VOICE = os.environ.get("TTS_VOICE", "hi-IN-SwaraNeural")


def to_wav(src, dst):
    result = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, dst],
                            capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr)


def speak_with_edge(text, output, voice, rate, pitch):
    import edge_tts

    async def run(mp3_path):
        await edge_tts.Communicate(text, voice, rate=rate, pitch=pitch).save(mp3_path)

    with tempfile.TemporaryDirectory() as tmp:
        mp3 = os.path.join(tmp, "voice.mp3")
        last_error = None
        for attempt in range(1, 4):                       # the service occasionally hiccups
            try:
                asyncio.run(run(mp3))
                if os.path.exists(mp3) and os.path.getsize(mp3) > 1000:
                    to_wav(mp3, output)
                    print(f"✅ Using TTS engine: edge-tts ({voice})")
                    return True
                last_error = "empty audio"
            except Exception as e:
                last_error = e
            print(f"⚠️ edge-tts attempt {attempt} failed: {last_error}")
    return False


def speak_with_espeak(text_path, output):
    if not shutil.which("espeak-ng"):
        return False
    with open(text_path, "r", encoding="utf-8") as f:
        has_hindi = any("\u0900" <= ch <= "\u097f" for ch in f.read())
    voice = "hi" if has_hindi else "en"
    result = subprocess.run(["espeak-ng", "-v", voice, "-s", "150", "-w", output, "-f", text_path],
                            capture_output=True, text=True)
    if result.returncode != 0:
        print(f"⚠️ espeak-ng failed: {result.stderr}")
        return False
    print("✅ Using TTS engine: espeak-ng (robotic fallback)")
    return True


def speak_with_pyttsx3(text, output):
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.setProperty("rate", 150)
        engine.save_to_file(text, output)
        engine.runAndWait()
        print("✅ Using TTS engine: pyttsx3")
        return True
    except Exception as e:
        print(f"⚠️ pyttsx3 failed: {e}")
        return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="content/script.txt", help="Path to script text file")
    parser.add_argument("--output", default="voice.wav", help="Output WAV file path")
    parser.add_argument("--engine", choices=["auto", "edge", "espeak", "pyttsx3"], default="auto")
    parser.add_argument("--voice", default=DEFAULT_VOICE, help="edge-tts voice name")
    parser.add_argument("--rate", default="-5%", help="Speech speed, e.g. -10%% slower, +10%% faster")
    parser.add_argument("--pitch", default="+0Hz", help="Pitch shift, e.g. +5Hz")
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

    order = {"auto": ["edge", "espeak", "pyttsx3"]}.get(args.engine, [args.engine])
    done = False
    for engine in order:
        if engine == "edge":
            done = speak_with_edge(text, args.output, args.voice, args.rate, args.pitch)
        elif engine == "espeak":
            done = speak_with_espeak(args.input, args.output)
        else:
            done = speak_with_pyttsx3(text, args.output)
        if done and os.path.exists(args.output) and os.path.getsize(args.output) > 1000:
            break
        done = False

    if not done:
        print("❌ No TTS engine produced audio.")
        sys.exit(1)

    print(f"✅ Voice-over saved to {args.output}")


if __name__ == "__main__":
    main()
