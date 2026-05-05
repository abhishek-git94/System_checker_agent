# agent/symptom_agent.py
import os
from dotenv import load_dotenv
from groq import Groq
from agent.prompts import SYSTEM_PROMPT

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_agent_response(user_input: str):
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
        return f"Arre! Thoda error aaya hai: {str(e)}"