import streamlit as st
import google.generativeai as genai

# Title
st.title("🗣️ Ishtyaque Bhai's AI Coach")

# API Key Connection
try:
    # Secrets se key uthana
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    
    # Is baar hum simple 'gemini-1.5-flash' use karenge 
    # Bina kisi beta version ke jhatke ke
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    user_input = st.chat_input("English ya Arabic mein kuch bolein...")
    
    if user_input:
        response = model.generate_content(user_input)
        st.write("AI Teacher:", response.text)
        
except Exception as e:
    st.error(f"Dhyan dein: {e}")
