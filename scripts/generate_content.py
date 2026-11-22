#!/usr/bin/env python3
"""
Generate Ayurvedic video content using built-in templates.
No API key required.
"""
import os
import random
import json

TOPICS = [
    {
        "title": "Instant Acidity Relief – Ayurvedic Ginger Tea",
        "script": "Namaste! Today we share a simple Ayurvedic remedy for acidity. Boil one cup of water, add a small piece of ginger and a squeeze of lemon. Drink this warm tea after meals to balance Pitta dosha and soothe your stomach. This natural home remedy has been used for generations. Try it today and feel the difference. Don't forget to like, subscribe, and hit the bell for more Ayurvedic wellness tips!",
        "description": "Learn how to balance Pitta dosha with this quick ginger-lemon tea for instant acidity relief. Not medical advice.",
        "tags": ["ayurveda", "acidity", "ginger tea", "pitta balance", "home remedy", "wellness", "natural cure"]
    },
    {
        "title": "Morning Dinacharya – Ayurvedic Daily Routine",
        "script": "Welcome to your Ayurvedic morning routine. Wake up before sunrise, scrape your tongue, drink warm water, and do a short self-massage with sesame oil. These simple steps activate your digestion and set a calm tone for the day. Follow this dinacharya daily for better energy and immunity. Subscribe for more daily Ayurveda tips.",
        "description": "A simple Ayurvedic morning dinacharya to start your day right. Not medical advice.",
        "tags": ["ayurveda", "dinacharya", "morning routine", "ayurvedic lifestyle", "wellness", "self care"]
    },
    {
        "title": "Turmeric Milk for Better Sleep",
        "script": "Struggling to sleep? Try golden milk. Warm a cup of milk, add half a teaspoon of turmeric, a pinch of black pepper, and a little honey. Drink it 30 minutes before bed. Turmeric calms the mind and supports restful sleep naturally. Sweet dreams!",
        "description": "Ayurvedic golden milk recipe for better sleep. Not medical advice.",
        "tags": ["ayurveda", "turmeric milk", "golden milk", "sleep aid", "home remedy", "wellness"]
    },
    {
        "title": "Triphala Detox Water",
        "script": "Detox gently with Triphala water. Soak one teaspoon of Triphala powder in a glass of water overnight. Strain and drink in the morning on an empty stomach. Triphala supports digestion and cleanses the body. Make it part of your weekly routine.",
        "description": "How to make Triphala detox water for gentle cleansing. Not medical advice.",
        "tags": ["ayurveda", "triphala", "detox water", "digestion", "cleanse", "wellness"]
    },
    {
        "title": "Nasya Oil for Clear Sinuses",
        "script": "Clear your sinuses with Nasya. Lie down and put two drops of warm sesame oil or Anu taila in each nostril. This ancient Ayurvedic practice lubricates the nasal passages and improves breathing. Do it once a day in the morning.",
        "description": "Ayurvedic Nasya oil technique for sinus relief. Not medical advice.",
        "tags": ["ayurveda", "nasya", "sinus relief", "sinuses", "wellness", "breathing"]
    },
]


DISCLAIMER = " This video is for general information only and is not medical advice. Please consult a qualified doctor before trying any remedy, especially if you are pregnant, on medication, or have a health condition."


def main():
    os.makedirs("content", exist_ok=True)
    topic = random.choice(TOPICS)
    topic = {**topic, "script": topic["script"] + DISCLAIMER}

    with open("content/title.txt", "w", encoding="utf-8") as f:
        f.write(topic["title"])
    with open("content/script.txt", "w", encoding="utf-8") as f:
        f.write(topic["script"])
    with open("content/description.txt", "w", encoding="utf-8") as f:
        f.write(topic["description"])
    with open("content/tags.txt", "w", encoding="utf-8") as f:
        f.write(", ".join(topic["tags"]))

    print(f"✅ Content generated: {topic['title']}")


if __name__ == "__main__":
    main()