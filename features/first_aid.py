# features/first_aid.py
from typing import List

FIRST_AID_GUIDES = {
    "fever": {
        "title": "Fever ( Bukhar)",
        "steps": [
            "Measure temperature with a thermometer",
            "If temperature is above 38°C, take paracetamol",
            "Drink plenty of water and fluids",
            "Take rest in a comfortable place",
            "Use a cool cloth on forehead if needed",
            "If fever persists for more than 3 days, see a doctor"
        ],
        "do": ["Drink water", "Take rest", "Take fever medicine"],
        "dont": ["Don't cover with heavy blankets", "Don't take Aspirin for children"]
    },
    "headache": {
        "title": "Headache (Sir dard)",
        "steps": [
            "Rest in a quiet, dark room",
            "Take a pain reliever like ibuprofen or paracetamol",
            "Apply cold pack on forehead for 15 minutes",
            "Massage temples gently",
            "Drink water - dehydration can cause headache",
            "If headache is severe or persists, consult doctor"
        ],
        "do": ["Rest", "Stay hydrated", "Take pain medicine"],
        "dont": ["Don't strain eyes", "Don't skip meals"]
    },
    "cold": {
        "title": "Common Cold (Sardi)",
        "steps": [
            "Get plenty of rest",
            "Drink warm fluids like tea, soup",
            "Use steam inhalation for congestion",
            "Take vitamin C or citrus fruits",
            "Use saline nasal drops",
            "Cover when going out in cold"
        ],
        "do": ["Drink warm fluids", "Rest", "Steam inhalation"],
        "dont": ["Don't go in cold", "Don't eat cold food"]
    },
    "cough": {
        "title": "Cough (Khansi)",
        "steps": [
            "Drink warm water with honey",
            "Take steam twice a day",
            "Avoid cold drinks and food",
            "Use cough syrup if needed",
            "Eat ginger or tulsi leaves",
            "If cough persists more than 2 weeks, see doctor"
        ],
        "do": ["Drink warm water with honey", "Steam", "Rest"],
        "dont": ["Don't eat cold items", "Don't smoke"]
    },
    "stomach_pain": {
        "title": "Stomach Pain (Pet dard)",
        "steps": [
            "Rest and avoid strenuous activity",
            "Drink water in small amounts",
            "Avoid solid food for a few hours",
            "Use heating pad on stomach",
            "Take antacid if acidity suspected",
            "See doctor if pain is severe or persists"
        ],
        "do": ["Rest", "Drink water", "Use heat pad"],
        "dont": ["Don't eat heavy food", "Don't lie down immediately after eating"]
    },
    "diarrhea": {
        "title": "Diarrhea (Dast)",
        "steps": [
            "Drink plenty of ORS solution or water",
            "Eat light food like rice, banana, toast",
            "Avoid dairy, fried, spicy food",
            "Take loperamide if needed",
            "Wash hands frequently",
            "See doctor if persists more than 2 days"
        ],
        "do": ["Drink ORS", "Eat light food", "Stay hydrated"],
        "dont": ["Don't eat dairy", "Don't eat spicy food"]
    },
    "vomiting": {
        "title": "Vomiting (Ulti)",
        "steps": [
            "Stop eating solid food temporarily",
            "Sip water slowly in small amounts",
            "Drink ginger tea or oral solution",
            "Rest with head elevated",
            "Gradually restart with light food",
            "See doctor if vomiting persists"
        ],
        "do": ["Sip water slowly", "Rest", "Drink ginger tea"],
        "dont": ["Don't eat immediately", "Don't lie flat"]
    },
    "burn": {
        "title": "Burn (Jalna)",
        "steps": [
            "Cool the burn under running water for 10-20 minutes",
            "Remove tight items before swelling",
            "Don't apply ice, butter, or toothpaste",
            "Cover with clean, non-stick bandage",
            "Take pain reliever if needed",
            "See doctor for severe burns"
        ],
        "do": ["Cool with water", "Cover with clean bandage", "Take pain medicine"],
        "dont": ["Don't apply ice", "Don't break blisters"]
    },
    "cut": {
        "title": "Cut/Wound (Kat)",
        "steps": [
            "Wash hands before touching wound",
            "Stop bleeding by applying pressure",
            "Clean wound with clean water",
            "Apply antiseptic ointment",
            "Cover with bandage",
            "Change bandage daily"
        ],
        "do": ["Clean wound", "Apply antiseptic", "Cover with bandage"],
        "dont": ["Don't use dirty hands", "Don't remove scabs"]
    },
    "choking": {
        "title": "Choking (Galay atakna)",
        "steps": [
            "Stay calm",
            "Cough forcefully to try to dislodge",
            "If coughing fails, perform Heimlich maneuver",
            "For pregnant women: chest thrusts",
            "For infants: back blows and chest thrusts",
            "Call emergency if object not removed"
        ],
        "do": ["Try to cough", "Heimlich maneuver", "Call 108 if needed"],
        "dont": ["Don't panic", "Don't put finger blindly"]
    },
    "sprain": {
        "title": "Sprain (Mootna)",
        "steps": [
            "Rest the injured area",
            "Apply ice wrapped in cloth for 15-20 mins",
            "Compress with elastic bandage",
            "Elevate the injured area",
            "Take pain reliever",
            "See doctor if severe swelling"
        ],
        "do": ["Rest", "Ice", "Compress", "Elevate"],
        "dont": ["Don't put weight on injured area", "Don't massage"]
    },
    "toothache": {
        "title": "Toothache (Danto mein dard)",
        "steps": [
            "Rinse mouth with warm salt water",
            "Take pain reliever like ibuprofen",
            "Apply clove oil on affected area",
            "Avoid very hot or cold food",
            "Use dental pain gel",
            "See dentist as soon as possible"
        ],
        "do": ["Salt water rinse", "Clove oil", "Pain medicine"],
        "dont": ["Don't eat sweet", "Don't ignore"]
    }
}

def get_first_aid(condition: str) -> str:
    condition = condition.lower()
    
    for key in FIRST_AID_GUIDES:
        if key in condition:
            guide = FIRST_AID_GUIDES[key]
            result = f"🚑 **{guide['title']}**\n\n"
            result += "**Steps:**\n"
            for i, step in enumerate(guide["steps"], 1):
                result += f"{i}. {step}\n"
            
            result += "\n**✅ Do:**\n"
            for item in guide["do"]:
                result += f"- {item}\n"
            
            result += "\n**❌ Don't:**\n"
            for item in guide["dont"]:
                result += f"- {item}\n"
            
            result += "\n⚠️ If condition is serious, consult a doctor immediately!"
            return result
    
    return "Sorry, I don't have first aid for this condition. Please consult a doctor."

def get_all_first_aid_conditions() -> List[str]:
    return list(FIRST_AID_GUIDES.keys())