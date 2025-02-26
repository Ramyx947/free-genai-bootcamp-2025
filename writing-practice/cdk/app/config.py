# Word categories organized by difficulty level
WORD_CATEGORIES = {
    "Beginner": {
        "Basic/Common Words": {
            "bună": "hello",
            "la revedere": "goodbye",
            "mulțumesc": "thank you",
            "da": "yes",
            "nu": "no",
            "te rog": "please",
            "bine": "good",
            "rău": "bad",
            "apă": "water",
            "pâine": "bread",
            "casă": "house",
            "masă": "table",
            "scaun": "chair",
            "carte": "book",
            "pisică": "cat",
            "câine": "dog"
        },
        "Food and Drinks": {
            "supă": "soup",
            "carne": "meat",
            "pește": "fish",
            "orez": "rice",
            "cartofi": "potatoes",
            "roșii": "tomatoes",
            "brânză": "cheese",
            "ouă": "eggs",
            "lapte": "milk",
            "cafea": "coffee",
            "ceai": "tea",
            "vin": "wine",
            "bere": "beer",
            "desert": "dessert",
            "fructe": "fruits",
            "legume": "vegetables",
            "ciocolată": "chocolate",
            "înghețată": "ice cream",
            "salată": "salad",
            "miere": "honey"
        }
    },
    "Intermediate": {
        "Travel and Transportation": {
            "aeroport": "airport",
            "avion": "airplane",
            "tren": "train",
            "autobuz": "bus",
            "taxi": "taxi",
            "hotel": "hotel",
            "cameră": "room",
            "plajă": "beach",
            "munte": "mountain",
            "parc": "park",
            "stradă": "street",
            "drum": "road",
            "hartă": "map",
            "bilet": "ticket",
            "pasaport": "passport",
            "bagaj": "luggage",
            "stație": "station",
            "centru": "center",
            "muzeu": "museum",
            "restaurant": "restaurant"
        },
        "Shopping and Money": {
            "magazin": "store",
            "piață": "market",
            "bani": "money",
            "preț": "price",
            "ieftin": "cheap",
            "scump": "expensive",
            "reducere": "discount",
            "portofel": "wallet",
            "card": "card",
            "factură": "bill"
        },
        "Time and Weather": {
            "timp": "time",
            "zi": "day",
            "noapte": "night",
            "dimineață": "morning",
            "seară": "evening",
            "soare": "sun",
            "ploaie": "rain",
            "zăpadă": "snow",
            "cald": "warm",
            "frig": "cold"
        }
    },
    "Advanced": {
        "Formal and Informal Expressions": {
            "bună ziua": {"translation": "good day"},
            "la mulți ani": {"translation": "happy birthday/happy new year"},
            "cu plăcere": {"translation": "you're welcome"},
            "scuze": {"translation": "sorry"},
            "îmi pare rău": {"translation": "I'm sorry"},
            "vă rog": {"translation": "please"},
            "te rog frumos": {"translation": "please"},
            "domnul": {"translation": "mister"},
            "doamna": {"translation": "madam"},
            "domnișoară": {"translation": "miss"},
            "cu respect": {"translation": "with respect"},
            "mulțumesc frumos": {"translation": "thank you very much"},
            "mersi": {"translation": "thanks"},
            "noapte bună": {"translation": "good night"},
            "pe curând": {"translation": "see you soon"},
            "pa": {"translation": "bye"},
            "salut": {"translation": "bye"},
            "servus": {"translation": "hi"},
            "la revedere": {"translation": "goodbye"},
            "toate cele bune": {"translation": "all the best"},
            "cu drag": {"translation": "with pleasure"}
        }
    }
}

# Flatten dictionaries for word selection
ROMANIAN_TO_ENGLISH = {}
for level in WORD_CATEGORIES.values():
    for category in level.values():
        for rom, eng in category.items():
            if isinstance(eng, dict):
                ROMANIAN_TO_ENGLISH[rom] = eng["translation"]
            else:
                ROMANIAN_TO_ENGLISH[rom] = eng

ALL_ROMANIAN_WORDS = list(ROMANIAN_TO_ENGLISH.keys())
ALL_ENGLISH_WORDS = list(ROMANIAN_TO_ENGLISH.values())

def get_category_for_word(word):
    """Find the category and difficulty level for a given word."""
    for difficulty, categories in WORD_CATEGORIES.items():
        for category, words in categories.items():
            if word in words or word in words.values():
                return difficulty, category
    return None, None
