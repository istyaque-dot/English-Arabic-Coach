import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import base64

# 1. Setup
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("API Key missing or error!")

# 2. UI Layout
st.title("🗣️ Ishtyaque Bhai's Mastery Coach")
st.write("Jamnagar to Global: Learn English & Arabic")

option = st.sidebar.selectbox("Kaunsi zubaan sikhni hai?", ("English", "Arabic"))
lang_code = 'en' if option == "English" else 'ar'

# 3. Chat Logic
user_text = st.chat_input(f"Talk to me in {option}...")

if user_text:
    with st.chat_message("user"):
        st.write(user_text)
    
    # AI Logic
    prompt = f"Teacher mode: User said '{user_text}'. Reply in {option}, correct mistakes, and give 1 better word."
    response = model.generate_content(prompt)
    reply = response.text
    
    with st.chat_message("assistant"):
        st.write(reply)
        
        # Voice Output
        tts = gTTS(text=reply, lang=lang_code)
        tts.save("voice.mp3")
        with open("voice.mp3", "rb") as f:
            data = base64.b64encode(f.read()).decode()
            st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{data}">', unsafe_allow_html=True)
