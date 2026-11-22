#!/usr/bin/env python3
"""
Generate Hinglish Ayurvedic video content using built-in templates.
No API key required.

IMPORTANT for the voice: write Hindi words in Devanagari and keep English words in Latin letters
(e.g. "Acidity की वजह से..."). Hindi neural voices read that mix naturally.
Romanized Hindi ("aap kaise hain") would be read with an English accent, so avoid it in "script".
Titles/descriptions/tags stay in English letters (the thumbnail font has no Devanagari).
"""
import os
import random
from disclaimer import SPOKEN, DESCRIPTION

TOPICS = [
    {
        "title": "Acidity? Try Dadi's Ginger Tea | Ayurvedic Tips in Hinglish",
        "script": "नमस्ते दोस्तों! Acidity की वजह से पेट में आग लगी है? दादी का एक आसान नुस्ख़ा सुनिए। एक कप पानी उबालिए, उसमें अदरक का छोटा टुकड़ा डालिए, और खाने के बाद गुनगुनी चाय पीजिए। Ayurveda में माना जाता है कि इससे पाचन को सहारा मिलता है। और हाँ, ये WhatsApp university वाला नुस्ख़ा नहीं है, ये घर का है! वीडियो पसंद आए तो like और subscribe ज़रूर करिए।",
        "description": "A fun Hinglish guide to a traditional Ayurvedic ginger tea that many families drink after meals.",
        "tags": ["ayurveda", "hinglish", "ginger tea", "acidity", "dadi ka nuskha", "home remedy", "wellness"],
    },
    {
        "title": "Ayurvedic Morning Routine (Dinacharya) in Hinglish",
        "script": "नमस्ते! सुबह उठते ही सबसे पहले फ़ोन देखते हैं ना? आज Ayurveda वाली सुबह try करते हैं। सूरज निकलने से पहले उठिए, जीभ साफ़ कीजिए, गुनगुना पानी पीजिए, और थोड़ी देर तिल के तेल से मालिश कीजिए। इसे dinacharya कहते हैं, यानी रोज़ का एक सरल routine। पहले ही दिन सब कुछ मत कीजिए, बस एक-एक आदत जोड़िए। Subscribe करना मत भूलिए!",
        "description": "A simple Ayurvedic dinacharya (daily routine) explained in Hinglish, one small habit at a time.",
        "tags": ["ayurveda", "hinglish", "dinacharya", "morning routine", "ayurvedic lifestyle", "wellness"],
    },
    {
        "title": "Haldi Doodh Before Bed? Golden Milk Explained | Hinglish",
        "script": "रात को नींद नहीं आ रही? Mobile तो रख दीजिए, पहले ये नुस्ख़ा सुनिए! एक कप गुनगुने दूध में आधा चम्मच हल्दी और एक चुटकी काली मिर्च डालिए। कई घरों में सोने से तीस मिनट पहले इसे पीने की परंपरा है। Ayurveda में इसे golden milk भी कहते हैं। ध्यान रखिए, हर किसी पर एक जैसा असर नहीं होता। शुभ रात्रि!",
        "description": "Golden milk (haldi doodh), a traditional bedtime drink in many Indian homes, explained in Hinglish.",
        "tags": ["ayurveda", "hinglish", "haldi doodh", "golden milk", "turmeric milk", "home remedy", "wellness"],
    },
    {
        "title": "Triphala Water Explained | Traditional Ayurvedic Drink | Hinglish",
        "script": "Triphala का नाम सुना है? ये तीन फलों से बना एक पारंपरिक Ayurvedic चूर्ण है: आँवला, बहेड़ा और हरड़। परंपरा में लोग इसे रात को पानी में भिगोकर सुबह पीते हैं, पाचन को सहारा देने के लिए। स्वाद? थोड़ा कड़वा, लेकिन ज़िंदगी भी तो कभी-कभी कड़वी होती है! गर्भावस्था में या दवाइयों के साथ, doctor की सलाह के बिना इसे मत लीजिए।",
        "description": "What is Triphala and how is it traditionally used? Explained in Hinglish, with safety notes.",
        "tags": ["ayurveda", "hinglish", "triphala", "digestion", "traditional medicine", "wellness"],
    },
    {
        "title": "What is Nasya? Ayurvedic Practice Explained | Hinglish",
        "script": "Nasya एक पारंपरिक Ayurvedic पद्धति है, जिसमें नाक में तेल की कुछ बूँदें डाली जाती हैं। इसे सही तरीक़ा सीखकर, किसी Ayurvedic doctor की सलाह से ही करना चाहिए। घर पर experiment करने से पहले ज़रूर पूछिए, क्योंकि नाक कोई science project नहीं है! ऐसे ही और Ayurveda की बातें सुनने के लिए subscribe कीजिए।",
        "description": "Nasya is a traditional Ayurvedic practice. This Hinglish explainer covers what it is and why to learn it from a practitioner.",
        "tags": ["ayurveda", "hinglish", "nasya", "ayurvedic practice", "wellness"],
    },
]


def main():
    os.makedirs("content", exist_ok=True)
    topic = random.choice(TOPICS)
    topic = {**topic,
             "script": topic["script"] + SPOKEN,
             "description": topic["description"] + DESCRIPTION}

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
