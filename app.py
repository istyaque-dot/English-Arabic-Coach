import streamlit as st
import google.generativeai as genai

st.title("🗣️ Ishtyaque Bhai's AI Coach")

try:
    # 1. API Key Setup
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    
    # Is line se hum 'v1' stable version ko force kar rahe hain
    genai.configure(api_key=API_KEY, transport='rest') 
    
    # 2. Model Setup (Stable Name)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    user_input = st.chat_input("English ya Arabic mein kuch bolein...")
    
    if user_input:
        # Simple reply test
        response = model.generate_content(user_input)
        st.write("AI Teacher:", response.text)
        
except Exception as e:
    # Agar abhi bhi error aaye toh poori detail yahan dikhegi
    st.error(f"Error Detail: {e}")
