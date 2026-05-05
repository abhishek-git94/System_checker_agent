# features/hinglish.py

HINDI_KEYWORDS = {
    "dard": "pain",
    "bukhar": "fever",
    "sir": "head",
    "pet": "stomach",
    "khansi": "cough",
    "zukham": "cold",
    "ult": "vomit",
    "dast": "diarrhea",
    "chaak": "itchy",
    "swar": "voice",
    "nak": "nose",
    "aankhen": "eyes",
    "kann": "ear",
    "haath": "hand",
    "pair": "legs",
    "teen": "three",
    "teen din": "three days",
    "ek": "one",
    "do": "two",
    "char": "four",
    "paanch": "five",
    "kitne": "how many",
    "kab": "when",
    "kyun": "why",
    "kaise": "how",
    "kya": "what",
    "kaun": "who",
    "kidhar": "where",
    "abhi": "now",
    "kal": "yesterday/tomorrow",
    "aaj": "today",
    "raat": "night",
    "din": "day",
    "subah": "morning",
    "shaam": "evening",
    "saam": "evening",
    "khaana": "food",
    "paani": "water",
    "tablet": "medicine",
    "dawa": "medicine",
    "doctor": "doctor",
    "bimaar": "sick",
    "thik": "fine",
    "behtar": "better",
    "bura": "bad",
    "zyada": "more",
    "kam": "less",
    "bada": "big",
    "chhota": "small",
    "garam": "hot",
    "thanda": "cold",
    "tej": "high/severe",
    "halka": "mild",
    "chalna": "walk",
    "sona": "sleep",
    "uthna": "get up",
    "baithna": "sit",
    "lena": "take",
    "dena": "give",
    "jana": "go",
    "aana": "come",
    "dekhna": "see",
    "sunna": "hear",
    "bolna": "speak",
    "saans": "breath",
    "floating": "float",
    "likhna": "write",
    "padhna": "read",
    "khana": "eat",
    "peena": "drink",
}

def detect_language(text):
    """
    Detect karta hai user Hinglish, Hindi ya English mein likh raha hai
    """
    text_lower = text.lower()
    hindi_count = sum(1 for word in HINDI_KEYWORDS.keys() if word in text_lower)
    hindi_char_count = sum(1 for char in text_lower if ord(char) > 127 and '\u0900' <= char <= '\u097F')
    
    if hindi_count > 2 or hindi_char_count > 3:
        return "hindi"
    elif hindi_count > 0:
        return "hinglish"
    else:
        return "english"

def convert_hinglish_to_english(text):
    """
    Hinglish keywords ko English mein convert karta hai
    """
    text_lower = text.lower()
    
    for hindi, english in HINDI_KEYWORDS.items():
        text_lower = text_lower.replace(hindi, english)
    
    return text_lower

def format_hindi_response(text):
    """
    Response ko basic Hindi formatting ke saath return karta hai
    """
    return text

def get_response_language(user_input):
    """
    User ke input ke based pe response ka language decide karta hai
    """
    return detect_language(user_input)