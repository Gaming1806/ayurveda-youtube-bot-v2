#!/usr/bin/env python3
"""
Get video footage.
- If a 'footage/' folder exists with MP4 files, pick one at random.
- Otherwise, generate a 10-second solid-color clip with ffmpeg.
No API key required.
"""
import os
import random
import shutil
import subprocess
import sys


def main():
    output = "footage.mp4"
    footage_dir = "footage"

    mp4_files = []
    if os.path.isdir(footage_dir):
        for fname in os.listdir(footage_dir):
            if fname.lower().endswith(".mp4"):
                mp4_files.append(os.path.join(footage_dir, fname))

    if mp4_files:
        chosen = random.choice(mp4_files)
        shutil.copy(chosen, output)
        print(f"✅ Using local footage: {chosen}")
    else:
        # Generate a simple orange background clip (1280x720, 10 seconds)
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi",
            "-i", "color=c=orange:s=1280x720:d=10",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            output,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ ffmpeg failed to generate footage:")
            print(result.stderr)
            sys.exit(1)
        print(f"✅ Generated placeholder footage: {output}")

    if not os.path.exists(output):
        print("❌ Footage file missing.")
        sys.exit(1)


if __name__ == "__main__":
    main()