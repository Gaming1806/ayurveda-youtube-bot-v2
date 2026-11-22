#!/usr/bin/env python3
"""
Combine footage and voice-over into a final MP4 using ffmpeg.
No API key required.
"""
import argparse
import os
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--footage", default="footage.mp4", help="Path to video footage")
    parser.add_argument("--audio", default="voice.wav", help="Path to voice-over WAV")
    parser.add_argument("--output", default="final_video.mp4", help="Output MP4 path")
    parser.add_argument("--duration", type=int, default=30, help="Target duration in seconds")
    args = parser.parse_args()

    if not os.path.exists(args.footage):
        print(f"❌ Footage not found: {args.footage}")
        sys.exit(1)
    if not os.path.exists(args.audio):
        print(f"❌ Audio not found: {args.audio}")
        sys.exit(1)

    cmd = [
        "ffmpeg", "-y",
        "-i", args.footage,
        "-i", args.audio,
        "-filter_complex",
        f"[0:v]scale=1280:720,setsar=1,trim=duration={args.duration}[vid];"
        f"[1:a]atrim=duration={args.duration}[aud]",
        "-map", "[vid]",
        "-map", "[aud]",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-shortest",
        args.output,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ ffmpeg failed to assemble video:")
        print(result.stderr)
        sys.exit(1)

    print(f"✅ Final video saved to {args.output}")


if __name__ == "__main__":
    main()