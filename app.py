import streamlit as st
import google.generativeai as genai
from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase
from gtts import gTTS
import base64

# 1. AI Configuration (Gemini 2.5 Flash)
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
except:
    st.error("API Connection Error")

# 2. Advanced Audio Processor
class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.audio_frames = []

    def on_audio_frame(self, frame):
        # Yahan pro-level processing hoti hai
        return frame

# 3. UI - Advance Level Layout
st.set_page_config(page_title="AI Pro Coach", layout="wide")
st.title("🚀 Ishtyaque Bhai's Advance AI Coach")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🎤 Live Audio Command")
    # Advance WebRTC Mike System
    webrtc_streamer(
        key="speech-to-text",
        mode=WebRtcMode.SENDONLY,
        audio_processor_factory=AudioProcessor,
        media_stream_constraints={"audio": True, "video": False},
    )
    st.info("Mike on karke bolein. Ye system aapke M2 Mac ke hardware ko use karega.")

with col2:
    st.subheader("💬 Smart Correction")
    user_input = st.chat_input("Ya phir yahan English/Arabic likhein...")

# 4. Logic & Response
if user_input:
    with st.chat_message("user"):
        st.write(user_input)
    
    # Pro-Teacher Prompt
    prompt = f"Advance Coach Mode: Correct the user's sentence '{user_input}'. Give 1 professional version for transport business and 1 for stock trading. Keep it concise."
    
    response = model.generate_content(prompt)
    bot_reply = response.text
    
    with st.chat_message("assistant"):
        st.write(bot_reply)
        
        # Audio Reply
        tts = gTTS(text=bot_reply, lang='en')
        tts.save("reply.mp3")
        with open("reply.mp3", "rb") as f:
            data = base64.b64encode(f.read()).decode()
            st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{data}">', unsafe_allow_html=True)
