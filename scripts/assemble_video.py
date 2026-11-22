#!/usr/bin/env python3
"""
Combine footage and voice-over into a final MP4 using ffmpeg.
The footage is looped as needed so the video lasts as long as the voice-over.
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
    parser.add_argument("--duration", type=int, default=0,
                        help="Optional maximum duration in seconds (0 = match the voice-over)")
    args = parser.parse_args()

    if not os.path.exists(args.footage):
        print(f"❌ Footage not found: {args.footage}")
        sys.exit(1)
    if not os.path.exists(args.audio):
        print(f"❌ Audio not found: {args.audio}")
        sys.exit(1)

    cmd = [
        "ffmpeg", "-y",
        "-stream_loop", "-1", "-i", args.footage,   # loop footage endlessly
        "-i", args.audio,
        # Fit into 1280x720 without stretching, padding with black bars
        "-vf", "scale=1280:720:force_original_aspect_ratio=decrease,"
               "pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1",
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-movflags", "+faststart",
        "-shortest",                                 # ends when the voice-over ends
    ]
    if args.duration > 0:
        cmd += ["-t", str(args.duration)]
    cmd.append(args.output)

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ ffmpeg failed to assemble video:")
        print(result.stderr)
        sys.exit(1)

    print(f"✅ Final video saved to {args.output}")


if __name__ == "__main__":
    main()
