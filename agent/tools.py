# agent/tools.py

import os
import googlemaps
from dotenv import load_dotenv
from langchain.tools import tool
from utils.disclaimer import get_severity_message

load_dotenv()

gmaps = googlemaps.Client(key=os.getenv("GOOGLE_PLACES_API_KEY"))

@tool
def find_nearby_doctors(location: str, specialty: str = "doctor") -> str:
    """
    Nearby doctors ya clinics dhundho Google Places se.
    location: city ya area name (jaise 'Indore, Madhya Pradesh')
    specialty: doctor type (jaise 'dermatologist', 'general physician')
    """
    try:
        # Location ko coordinates mein convert karo
        geocode = gmaps.geocode(location)
        if not geocode:
            return "Location nahi mili. Please sahi location batao."
        
        lat = geocode[0]['geometry']['location']['lat']
        lng = geocode[0]['geometry']['location']['lng']
        
        # Nearby doctors dhundo
        places = gmaps.places_nearby(
            location=(lat, lng),
            radius=5000,  # 5km radius
            keyword=specialty,
            type='doctor'
        )
        
        if not places['results']:
            return "Aapke paas koi doctor nahi mila. Radius badha ke try karo."
        
        # Top 5 doctors format karo
        result = f"🏥 Aapke paas {specialty} doctors:\n\n"
        for i, place in enumerate(places['results'][:5], 1):
            name = place.get('name', 'N/A')
            address = place.get('vicinity', 'Address nahi mila')
            rating = place.get('rating', 'No rating')
            open_now = place.get('opening_hours', {}).get('open_now', None)
            
            status = "🟢 Abhi khula hai" if open_now else "🔴 Abhi band hai" if open_now is False else "⚪ Timing pata nahi"
            
            result += f"{i}. *{name}*\n"
            result += f"   📍 {address}\n"
            result += f"   ⭐ Rating: {rating}\n"
            result += f"   {status}\n\n"
        
        return result
        
    except Exception as e:
        return f"Doctors dhundhne mein problem aayi: {str(e)}"


@tool
def find_emergency_hospitals(location: str) -> str:
    """
    Nearest emergency hospitals dhundho.
    location: city ya area name
    """
    try:
        geocode = gmaps.geocode(location)
        if not geocode:
            return "Location nahi mili."
        
        lat = geocode[0]['geometry']['location']['lat']
        lng = geocode[0]['geometry']['location']['lng']
        
        # Emergency hospitals dhundo
        places = gmaps.places_nearby(
            location=(lat, lng),
            radius=10000,  # 10km radius emergency ke liye
            keyword="emergency hospital",
            type='hospital'
        )
        
        if not places['results']:
            return "Koi hospital nahi mila. 108 call karo abhi!"
        
        result = "🚨 NEAREST EMERGENCY HOSPITALS:\n\n"
        for i, place in enumerate(places['results'][:3], 1):
            name = place.get('name', 'N/A')
            address = place.get('vicinity', 'N/A')
            rating = place.get('rating', 'N/A')
            
            result += f"{i}. *{name}*\n"
            result += f"   📍 {address}\n"
            result += f"   ⭐ {rating}\n\n"
        
        result += "\n🚨 Emergency mein 108 call karo!"
        return result
        
    except Exception as e:
        return f"Error: {str(e)}\n🚨 108 call karo abhi!"


@tool
def assess_severity(symptoms: str) -> str:
    """
    Symptoms ke basis pe severity assess karo.
    symptoms: user ke symptoms string mein
    """
    symptoms_lower = symptoms.lower()
    
    # Emergency keywords
    emergency_keywords = [
        "seene mein dard", "chest pain", "saans nahi", "breathing problem",
        "behosh", "unconscious", "bahut zyada khoon", "heavy bleeding",
        "stroke", "paralysis", "laqwa"
    ]
    
    # High severity keywords
    high_keywords = [
        "tej bukhar", "high fever", "104", "105", "ulti", "vomiting",
        "dast", "diarrhea", "bahut dard", "severe pain"
    ]
    
    # Medium keywords
    medium_keywords = [
        "bukhar", "fever", "sir dard", "headache", "khansi", "cough",
        "gala dard", "throat pain", "pet dard", "stomach pain"
    ]
    
    for keyword in emergency_keywords:
        if keyword in symptoms_lower:
            return get_severity_message("emergency")
    
    for keyword in high_keywords:
        if keyword in symptoms_lower:
            return get_severity_message("high")
    
    for keyword in medium_keywords:
        if keyword in symptoms_lower:
            return get_severity_message("medium")
    
    return get_severity_message("low")


# Saare tools ki list
ALL_TOOLS = [
    find_nearby_doctors,
    find_emergency_hospitals,
    assess_severity
]