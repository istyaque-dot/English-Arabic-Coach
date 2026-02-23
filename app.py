import streamlit as st
import google.generativeai as genai

st.title("🗣️ AI Mastery Coach")

try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    
    # Forceful model selection
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    
    user_input = st.chat_input("English ya Arabic mein kuch bolein...")
    
    if user_input:
        response = model.generate_content(user_input)
        st.write("AI Teacher:", response.text)
        
except Exception as e:
    # Agar abhi bhi error aaye toh hum model list print karenge
    st.error(f"Error: {e}")
    if "404" in str(e):
        st.write("Checking available models...")
        available_models = [m.name for m in genai.list_models()]
        st.write(available_models)
