import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("❌ API key not found! Please set GEMINI_API_KEY in your .env file.")
    st.stop()

genai.configure(api_key=api_key)

# Create model
model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize session state for conversation
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# Streamlit UI
st.title("🤖 Customer Assistance Chatbot")
st.markdown("Ask me anything about your order, returns, or support!")

# Display previous conversation history first
for msg in st.session_state.chat.history:
    if msg.role == "model":
        st.chat_message("assistant").markdown(msg.parts[0].text)
    else:
        st.chat_message("user").markdown(msg.parts[0].text)

# Chat input box
user_input = st.chat_input("Type your message here...")

if user_input:
    # Show user message
    st.chat_message("user").markdown(user_input)

    # Get response from Gemini
    response = st.session_state.chat.send_message(user_input)

    # Show assistant response
    st.chat_message("assistant").markdown(response.text)
