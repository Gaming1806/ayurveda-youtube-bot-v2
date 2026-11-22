"""
Single source of truth for all disclaimer wording.
Place this file at: scripts/disclaimer.py
"""

TEXT = "The content is educational and not medical advice."

# Read aloud at the end of the voice-over
SPOKEN = " " + TEXT

# Shown across the bottom of the video for its whole length
ON_SCREEN_SHORT = TEXT

# Shown large for the first few seconds (one line per list item)
ON_SCREEN_INTRO = [
    "DISCLAIMER",
    TEXT,
]
INTRO_SECONDS = 4

# Appended to the YouTube description
DESCRIPTION = "\n\nDISCLAIMER: " + TEXT
