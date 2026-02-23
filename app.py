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
    st.error("Setup Error!")

# 2. Audio Out Function (AI ki awaaz)
def speak(text, lang='en'):
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save("voice.mp3")
        with open("voice.mp3", "rb") as f:
            data = base64.b64encode(f.read()).decode()
            st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{data}">', unsafe_allow_html=True)
    except:
        pass

# 3. Simple UI
st.title("🗣️ Ishtyaque Bhai's Voice Coach")
language = st.sidebar.radio("Zubaan chunein:", ("English", "Arabic"))
lang_code = 'en' if language == "English" else 'ar'

# Mike Input Section
st.write("Mike dabayein aur bolein:")
audio_input = mic_recorder(start_prompt="🎤 Bolna shuru karein", stop_prompt="🛑 Rukiye", key='recorder')

user_input = ""
if audio_input:
    # Voice to Text conversion check (Optional placeholder for transcription)
    # Abhi ke liye hum chat input ko hi main rakhte hain jab tak voice logic fully set na ho
    pass

chat_input = st.chat_input(f"Ya yahan {language} mein likhein...")
final_input = chat_input # Filhaal typing se hi AI ko input dete hain

if final_input:
    with st.chat_message("user"):
        st.write(final_input)
    
    prompt = f"Act as a simple {language} coach. User said: '{final_input}'. If there is a mistake, correct it in 1 VERY SHORT sentence. If no mistake, just reply naturally in 5-6 words. No hard words."
    
    try:
        response = model.generate_content(prompt)
        bot_reply = response.text
        
        with st.chat_message("assistant"):
            st.write(bot_reply)
        
        speak(bot_reply, lang=lang_code)
    except:
        st.error("AI connection error.")
