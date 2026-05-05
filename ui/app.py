# ui/app.py
import sys
import os
import io
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from agent.symptom_agent import get_agent_response

try:
    from faster_whisper import WhisperModel
    WHISPER_AVAILABLE = True
except:
    WHISPER_AVAILABLE = False

st.set_page_config(page_title="HealthBuddy", page_icon="🏥", layout="centered")

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
    }
    .main-title {
        text-align: center;
        font-size: 2.5rem;
        color: #1e3a5f;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        text-align: center;
        color: #5a7a9a;
        margin-bottom: 2rem;
    }
    .disclaimer {
        text-align: center;
        color: #888;
        font-size: 0.8rem;
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🏥 HealthBuddy</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">AI-Powered Symptom Checker | Voice Enabled</p>', unsafe_allow_html=True)

if WHISPER_AVAILABLE:
    @st.cache_resource
    def load_whisper_model():
        return WhisperModel("base", device="cpu", compute_type="int8")
    model = load_whisper_model()
else:
    import speech_recognition
    recognizer = speech_recognition.Recognizer()

if "messages" not in st.session_state:
    st.session_state.messages = []

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    audio_data = st.audio_input("🎤 Click to Speak", key="audio_input")

if audio_data:
    with st.spinner("🔄 Processing..."):
        try:
            audio_bytes = audio_data.read()
            
            if WHISPER_AVAILABLE:
                segments, info = model.transcribe(
                    io.BytesIO(audio_bytes),
                    language="en",
                    beam_size=5,
                    vad_filter=True
                )
                text = " ".join([seg.text for seg in segments]).strip()
            else:
                with speech_recognition.AudioFile(io.BytesIO(audio_bytes)) as source:
                    audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio, language="en-IN")
            
            if text:
                st.session_state.messages.append({"role": "user", "content": text})
                with st.chat_message("user", avatar="🧑"):
                    st.markdown(text)
                
                with st.chat_message("assistant", avatar="🏥"):
                    with st.spinner("🤔 Thinking..."):
                        response = get_agent_response(text)
                    st.markdown(response)
                
                st.session_state.messages.append({"role": "assistant", "content": response})
            else:
                st.warning("⚠️ Kuch detect nahi hua")
                
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

st.divider()

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🧑" if message["role"] == "user" else "🏥"):
        st.markdown(message["content"])

if prompt := st.chat_input("💬 Type your symptoms here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(prompt)
    
    with st.chat_message("assistant", avatar="🏥"):
        with st.spinner("🤔 Thinking..."):
            response = get_agent_response(prompt)
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

st.markdown('<p class="disclaimer">⚠️ Disclaimer: This is an AI assistant. Please consult a doctor for proper diagnosis.</p>', unsafe_allow_html=True)