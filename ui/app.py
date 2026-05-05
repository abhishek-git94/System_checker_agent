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

st.set_page_config(
    page_title="HealthBuddy AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: #0d1117;
    }
    
    .main-container {
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .header {
        background: linear-gradient(135deg, #1a1f36 0%, #0d1117 100%);
        padding: 2rem;
        border-radius: 16px;
        border: 1px solid #30363d;
        margin-bottom: 2rem;
    }
    
    .header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #58a6ff, #7ee787);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    
    .header p {
        color: #8b949e;
        font-size: 1rem;
        margin-top: 0.5rem;
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-bottom: 2rem;
    }
    
    .feature-card {
        background: #161b22;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #30363d;
        text-align: center;
    }
    
    .feature-card h3 {
        color: #58a6ff;
        font-size: 1rem;
        margin: 0;
    }
    
    .feature-card p {
        color: #8b949e;
        font-size: 0.8rem;
        margin-top: 0.5rem;
    }
    
    .chat-container {
        background: #161b22;
        border-radius: 16px;
        border: 1px solid #30363d;
        padding: 1rem;
    }
    
    .user-message {
        background: linear-gradient(135deg, #1f3d5c 0%, #1a1f36 100%);
        padding: 1rem;
        border-radius: 12px 12px 12px 0;
        border-left: 3px solid #58a6ff;
        margin: 1rem 0;
        color: #ffffff !important;
    }
    
    .bot-message {
        background: #21262d;
        padding: 1rem;
        border-radius: 12px 12px 0 12px;
        border-right: 3px solid #7ee787;
        margin: 1rem 0;
        color: #e6edf3 !important;
    }
    
    .input-container {
        background: #161b22;
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid #30363d;
    }
    
    .voice-btn {
        background: linear-gradient(135deg, #238636 0%, #2ea043 100%);
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        color: white;
        cursor: pointer;
        font-weight: 500;
    }
    
    .divider {
        border: none;
        border-top: 1px solid #30363d;
        margin: 2rem 0;
    }
    
    .stats-bar {
        display: flex;
        justify-content: space-around;
        background: #161b22;
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 2rem;
    }
    
    .stat {
        text-align: center;
    }
    
    .stat-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #58a6ff;
    }
    
    .stat-label {
        font-size: 0.8rem;
        color: #8b949e;
    }
    
    .sidebar-menu {
        background: #161b22;
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 1rem;
    }
    
    .menu-item {
        padding: 0.75rem 1rem;
        border-radius: 8px;
        color: #c9d1d9;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .menu-item:hover {
        background: #21262d;
    }
    
    .menu-item.active {
        background: #1f3d5c;
        color: #58a6ff;
    }
    
    @keyframes pulse {
        0% { opacity: 0.5; }
        50% { opacity: 1; }
        100% { opacity: 0.5; }
    }
    
    .loading {
        animation: pulse 1.5s infinite;
        color: #58a6ff;
    }
    
    .stMarkdown {
        color: #e6edf3 !important;
    }
    
    .stMarkdown p {
        color: #e6edf3 !important;
    }
    
    [data-testid="stMarkdownContainer"] p {
        color: #e6edf3 !important;
        line-height: 1.6;
    }
    
    div[data-testid="stChatMessageContent"] {
        color: #e6edf3 !important;
    }
    
    div[data-testid="stChatMessageContent"] p {
        color: #e6edf3 !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-container">
    <div class="header">
        <h1>🤖 HealthBuddy AI</h1>
        <p>Your AI-Powered Health Assistant | Powered by Groq + Llama 3.1</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="feature-grid">
    <div class="feature-card">
        <h3>🩺 Symptom Analysis</h3>
        <p>AI-powered symptom checking</p>
    </div>
    <div class="feature-card">
        <h3>🎤 Voice Input</h3>
        <p>Speak your symptoms</p>
    </div>
    <div class="feature-card">
        <h3>💊 Medicine Reminder</h3>
        <p>Track your medicines</p>
    </div>
    <div class="feature-card">
        <h3>🚑 First Aid Guide</h3>
        <p>Emergency assistance</p>
    </div>
</div>
""", unsafe_allow_html=True)

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

if "stats" not in st.session_state:
    st.session_state.stats = {"queries": 0, "first_aid": 0, "medicines": 0}

st.markdown("### 💬 Chat")

col1, col2 = st.columns([6, 1])
with col2:
    audio_data = st.audio_input("", key="audio_input", label_visibility="collapsed")

if audio_data:
    with st.spinner("🔄 Processing voice..."):
        try:
            audio_bytes = audio_data.read()
            
            if WHISPER_AVAILABLE:
                segments, info = model.transcribe(io.BytesIO(audio_bytes), language="en", beam_size=5, vad_filter=True)
                text = " ".join([seg.text for seg in segments]).strip()
            else:
                with speech_recognition.AudioFile(io.BytesIO(audio_bytes)) as source:
                    audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio, language="en-IN")
            
            if text:
                st.session_state.messages.append({"role": "user", "content": text})
                st.session_state.stats["queries"] += 1
                if "first aid" in text.lower():
                    st.session_state.stats["first_aid"] += 1
                if "medicine" in text.lower():
                    st.session_state.stats["medicines"] += 1
                
                with st.chat_message("user", avatar="👤"):
                    st.markdown(text)
                
                with st.chat_message("assistant", avatar="🤖"):
                    with st.spinner("🤔 Thinking..."):
                        response = get_agent_response(text)
                    st.markdown(response)
                
                st.session_state.messages.append({"role": "assistant", "content": response})
            else:
                st.warning("⚠️ Could not detect speech")
                
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="👤" if message["role"] == "user" else "🤖"):
        st.markdown(message["content"])

if prompt := st.chat_input("💬 Type your symptoms here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.stats["queries"] += 1
    if "first aid" in prompt.lower():
        st.session_state.stats["first_aid"] += 1
    if "medicine" in prompt.lower():
        st.session_state.stats["medicines"] += 1
    
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("🤔 Thinking..."):
            response = get_agent_response(prompt)
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

st.markdown("---")

st.markdown(f"""
<div style="display: flex; justify-content: space-around; text-align: center; color: #8b949e; font-size: 0.9rem;">
    <div>💬 {st.session_state.stats['queries']} Queries</div>
    <div>🚑 {st.session_state.stats['first_aid']} First Aid</div>
    <div>💊 {st.session_state.stats['medicines']} Medicines</div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

st.markdown("""
<div style="text-align: center; color: #484f58; font-size: 0.75rem; padding: 1rem;">
    ⚠️ <b>Disclaimer:</b> This is an AI assistant. Not a substitute for professional medical advice.<br>
    In case of emergency, call 108 immediately.
</div>
""", unsafe_allow_html=True)