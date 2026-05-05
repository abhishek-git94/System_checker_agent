# features/first_aid.py
from agent.prompts import FIRST_AID_PROMPT

def get_first_aid_instructions(condition: str):
    # Yeh function agent call karega jab use lagega ki immediate help chahiye
    # Abhi ke liye hum prompt return kar rahe hain, baad mein isse enhance kar sakte hain
    return f"First Aid for {condition}: {FIRST_AID_PROMPT}"