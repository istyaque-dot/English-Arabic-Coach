import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import base64
from streamlit_mic_recorder import mic_recorder

# 1. API Setup
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    st.error("Setup Error! Check API Key.")

# 2. Audio Out Function (AI Reply)
def speak(text, lang='en'):
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save("voice.mp3")
        with open("voice.mp3", "rb") as f:
            data = base64.b64encode(f.read()).decode()
            st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{data}">', unsafe_allow_html=True)
    except:
        pass

# 3. UI Section
st.title("🗣️ Ishtyaque Bhai's English-Arabic Coach")
st.write("Jamnagar to Global Mastery")

language = st.sidebar.radio("Zubaan chunein:", ("English", "Arabic"))
lang_code = 'en' if language == "English" else 'ar'

# Mike Input Section
st.subheader("🎤 Speak or Type")
audio = mic_recorder(
    start_prompt="🎤 Mike On (Click to Speak)",
    stop_prompt="🛑 Stop (Click to Finish)",
    key='recorder'
)

# Agar Mike se kuch record hua
if audio:
    st.audio(audio['bytes'])
    st.info("Awaaz record ho gayi hai! Abhi ke liye AI text input par behtar kaam karta hai. Niche box mein type karein.")

# Text Input (Main Chat)
user_input = st.chat_input(f"{language} mein likhein...")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)
    
    # Simple Prompt
    prompt = f"Simple coach: Correct mistakes in '{user_input}'. Reply in 1 short sentence. No hard words."
    
    try:
        response = model.generate_content(prompt)
        bot_reply = response.text
        
        with st.chat_message("assistant"):
            st.write(bot_reply)
        
        speak(bot_reply, lang=lang_code)
    except:
        st.error("AI Busy!")
