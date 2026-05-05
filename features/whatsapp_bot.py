# features/whatsapp_bot.py
from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_whatsapp_message(to_number, message):
    """
    WhatsApp message bhejta hai
    """
    try:
        whatsapp_msg = client.messages.create(
            body=message,
            from_=TWILIO_WHATSAPP_NUMBER,
            to=f"whatsapp:{to_number}"
        )
        return whatsapp_msg.sid
    except Exception as e:
        return f"Error: {str(e)}"

def handle_incoming_message(from_number, message_body):
    """
    Incoming WhatsApp message handle karta hai
    """
    from agent.symptom_agent import get_agent_response
    
    response = get_agent_response(message_body)
    send_whatsapp_message(from_number, response)
    return response

def start_whatsapp_server():
    """
    Flask server start karta hai WhatsApp webhook ke liye
    """
    from flask import Flask, request
    
    app = Flask(__name__)
    
    @app.route("/webhook", methods=["POST"])
    def webhook():
        incoming_msg = request.form.get("Body")
        from_num = request.form.get("From")
        
        if incoming_msg and from_num:
            handle_incoming_message(from_num, incoming_msg)
        
        return "OK"
    
    print("WhatsApp bot server running on port 5000...")
    app.run(port=5000, debug=True)