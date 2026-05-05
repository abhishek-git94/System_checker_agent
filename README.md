# HealthBuddy - AI Symptom Checker

An AI-powered health assistant that helps users check their symptoms and get health guidance.

## Features

- **Symptom Analysis** - Describe your symptoms and get AI-powered analysis
- **Voice Input** - Speak directly using voice recognition (Whisper)
- **Lab Report Analysis** - Upload blood test reports for analysis
- **Emergency Detection** - Identifies critical conditions and suggests calling 108
- **Doctor Discovery** - Find nearby doctors and hospitals using Google Maps
- **Hinglish Support** - Understands Hindi-English mixed language
- **WhatsApp Integration** - Access via WhatsApp bot
- **Modern UI** - Clean, professional Streamlit interface

## Tech Stack

- **Python** - Core language
- **Groq (Llama 3.1)** - AI language model
- **Streamlit** - Web UI
- **Faster Whisper** - Voice recognition
- **Google Maps API** - Location services
- **Twilio** - WhatsApp integration

## Installation

1. Clone the repository:
```bash
git clone https://github.com/abhishek-git94/System_checker_agent.git
cd System_checker_agent
```

2. Create a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install additional packages:
```bash
pip install streamlit groq langchain-groq googlemaps speechrecognition faster-whisper twilio flask
```

5. Create a `.env` file:
```
GROQ_API_KEY=your_groq_api_key
GOOGLE_PLACES_API_KEY=your_google_maps_api_key
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

## Usage

Run the web UI:
```bash
python main.py ui
```

Then open http://localhost:8502 in your browser.

## API Keys Required

1. **Groq API Key** - Get from https://console.groq.com/
2. **Google Places API Key** - Get from Google Cloud Console
3. **Twilio** (optional) - For WhatsApp bot

## Disclaimer

This is an AI assistant and NOT a doctor. Always consult a healthcare professional for proper diagnosis. In case of emergency, call 108 immediately.

## License

MIT License

## Author

Abhishek Pal