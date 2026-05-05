 # utils/disclaimer.py

MEDICAL_DISCLAIMER = """
⚠️ *IMPORTANT DISCLAIMER*
- Yeh ek AI-based tool hai, doctor nahi
- Yahan di gayi information sirf general guidance ke liye hai
- Kisi bhi serious symptom mein turant doctor se milo
- Emergency mein 108 call karo
"""

SEVERITY_MESSAGES = {
    "low": "🟢 Ghabrao mat — ghar pe rest karo, paani piyo.",
    "medium": "🟡 Doctor se milna better rahega 1-2 din mein.",
    "high": "🔴 Jaldi doctor ke paas jao — der mat karo!",
    "emergency": "🚨 EMERGENCY! Abhi 108 call karo ya nearest hospital jao!"
}

def get_disclaimer():
    return MEDICAL_DISCLAIMER

def get_severity_message(level: str):
    return SEVERITY_MESSAGES.get(level, SEVERITY_MESSAGES["low"])
