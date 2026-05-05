# features/voice_input.py
import speech_recognition as sr
import pyttsx3

recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

def listen_to_speech(timeout=5):
    """
    User ki speech ko text mein convert karta hai
    """
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=timeout)
            text = recognizer.recognize_google(audio, language="en-IN")
            return text
    except sr.WaitTimeoutError:
        return "Timeout: Kuch bolo toh sunu"
    except sr.UnknownValueError:
        return "Samjha nahi. Phir se try karo"
    except Exception as e:
        return f"Error: {str(e)}"

def speak_text(text):
    """
    Text ko audio mein convert karke sunata hai
    """
    try:
        tts_engine.say(text)
        tts_engine.runAndWait()
    except Exception as e:
        print(f"TTS Error: {str(e)}")

def get_voice_input():
    """
    Voice input lene ka main function
    """
    return listen_to_speech()

def speak_response(text):
    """
    Response ko audio mein sunane ke liye
    """
    speak_text(text)