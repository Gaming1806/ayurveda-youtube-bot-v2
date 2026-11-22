#!/usr/bin/env python3
"""
Generate a 1280x720 YouTube thumbnail using Pillow.
No API key required.
"""
import argparse
import os
from PIL import Image, ImageDraw, ImageFont


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="content/title.txt", help="Path to title text file")
    parser.add_argument("--output", default="thumbnail.jpg", help="Output image path")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"⚠️ Title file not found: {args.input} - using default title")
        title = "Ayurvedic Wellness Tips"
    else:
        with open(args.input, "r", encoding="utf-8") as f:
            title = f.read().strip()
        if not title:
            title = "Ayurvedic Wellness Tips"

    # Create image
    img = Image.new("RGB", (1280, 720), color=(230, 126, 34))  # orange
    draw = ImageDraw.Draw(img)

    # Try to load a truetype font; fall back to default
    font = None
    for font_path in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "C:\\Windows\\Fonts\\arial.ttf",
    ]:
        if os.path.exists(font_path):
            try:
                font = ImageFont.truetype(font_path, 60)
                break
            except Exception:
                continue

    if font is None:
        font = ImageFont.load_default()

    # Wrap text if too long (simple split)
    max_width = 1100
    words = title.split()
    lines = []
    current = ""
    for word in words:
        test = f"{current} {word}".strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)

    # Calculate total height
    line_height = 70
    total_h = len(lines) * line_height
    y = (720 - total_h) // 2

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        w = bbox[2] - bbox[0]
        x = (1280 - w) // 2
        draw.text((x, y), line, fill=(255, 255, 255), font=font,
                  stroke_width=3, stroke_fill=(60, 30, 0))
        y += line_height

    img.save(args.output, "JPEG", quality=90)
    print(f"✅ Thumbnail saved to {args.output}")


if __name__ == "__main__":
    main()