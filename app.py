import streamlit as st
import google.generativeai as genai

# --- 1. WEB UI SETUP ---
st.set_page_config(page_title="HealthBot AI", page_icon="🩺", layout="centered")

# Safe, professional styling that won't break your chat text
st.markdown("""
<style>
    /* Professional Gradient Title */
    .main-title {
        text-align: center;
        font-size: 3.5rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #0056b3, #00d2ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding-bottom: 5px;
        margin-bottom: 0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    /* Clean Subtitle */
    .sub-title {
        text-align: center;
        font-size: 1.1rem;
        font-weight: 400;
        color: #6c757d;
        margin-bottom: 30px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# Display Headers
st.markdown('<h1 class="main-title">🩺 HealthBot AI</h1>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Your Professional Clinical Assistant</div>', unsafe_allow_html=True)
st.divider()

# --- 2. AI CONFIGURATION ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except (KeyError, FileNotFoundError):
    # PASTE YOUR ACTUAL API KEY INSIDE THE QUOTES BELOW FOR LOCAL TESTING
    API_KEY = "AIzaSyBQ-ELkLWeI4uCtq2CGLVLZgQqBqJHjHJg"  

genai.configure(api_key=API_KEY)

system_instruction = """
You are an intelligent, empathetic medical AI assistant similar to LiveHealthily. 
Your goal is to help users understand their symptoms, provide general health information, and offer wellness advice.
Always be polite, professional, and clear. 
Crucial Rule: You must always remind the user that you are an AI, not a doctor, and that they should consult a healthcare professional for actual medical diagnoses or emergencies.
"""

model = genai.GenerativeModel(
    'gemini-2.5-flash',
    system_instruction=system_instruction
)

# --- 3. CHAT INTERFACE ---
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

for message in st.session_state.chat_session.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

def stream_parser(stream_response):
    for chunk in stream_response:
        if chunk.text:
            yield chunk.text

if user_input := st.chat_input("E.g., What are the best home remedies for a sore throat?"):
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        response = st.session_state.chat_session.send_message(user_input, stream=True)

        st.write_stream(stream_parser(response))
