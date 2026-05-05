# agent/symptom_agent.py
import os
from dotenv import load_dotenv
from groq import Groq
from agent.prompts import SYSTEM_PROMPT
from features.medicine_reminder import add_medicine, get_todays_schedule, format_medicine_list, remove_medicine
from features.first_aid import get_first_aid

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_agent_response(user_input: str):
    user_input_lower = user_input.lower()
    
    if "medicine" in user_input_lower and ("add" in user_input_lower or "schedule" in user_input_lower):
        parts = user_input.split()
        return "To add medicine, tell me: Medicine name, dosage, time (morning/evening/night)"
    
    if "my medicine" in user_input_lower or "today's schedule" in user_input_lower or "medicine schedule" in user_input_lower:
        return get_todays_schedule()
    
    if "first aid" in user_input_lower or "emergency" in user_input_lower:
        conditions = ["fever", "headache", "cold", "cough", "burn", "cut", "choking", "stomach pain", "diarrhea", "vomiting", "sprain", "toothache"]
        for cond in conditions:
            if cond in user_input_lower:
                return get_first_aid(cond, "english" if user_input.isascii() else "hinglish")
        return "For which condition do you need first aid? I can help with: fever, headache, cold, cough, burn, cut, choking, stomach pain, diarrhea, vomiting, sprain, toothache"
    
    try:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]
        
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.1
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error: {str(e)}"