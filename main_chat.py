import streamlit as st
import google.generativeai as genai
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Omar AI | ذكاء عمر الشاوش",
    page_icon="🚀",
    layout="wide",
)

# --- PREMIUM DARK CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&family=Noto+Sans+Arabic:wght@400;600&display=swap');
    
    :root {
        --primary-green: #10a37f;
        --accent-blue: #00d2ff;
        --dark-bg: #0b0e11;
        --sidebar-bg: #171d24;
        --chat-user-bg: #1c232d;
        --chat-bot-bg: #111821;
        --text-color: #e1e1e1;
    }

    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0b0e11 0%, #171d24 100%) !important;
        color: var(--text-color) !important;
        font-family: 'Outfit', 'Noto Sans Arabic', sans-serif !important;
    }

    .main .block-container {
        max-width: 900px;
        padding-top: 3rem;
        padding-bottom: 7rem;
    }

    [data-testid="stSidebar"] {
        background-color: var(--sidebar-bg) !important;
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    
    .stChatMessage {
        margin: 1.2rem 0 !important;
        border-radius: 12px !important;
    }

    [data-testid="stChatMessageUser"] {
        background: var(--chat-user-bg) !important;
        border: 1px solid rgba(255,255,255,0.05) !important;
    }

    [data-testid="stChatMessageAssistant"] {
        background: var(--chat-bot-bg) !important;
        border-left: 4px solid var(--primary-green) !important;
    }

    .stMarkdown p {
        font-size: 1.15rem;
        line-height: 1.8;
    }
    
    h1, h2, h3 {
        background: linear-gradient(90deg, #10a37f, #00d2ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        text-align: center;
    }

    .stChatInputContainer {
        border-radius: 25px !important;
        background: rgba(28, 35, 45, 0.9) !important;
        backdrop-filter: blur(10px) !important;
    }

    .footer-note {
        font-size: 0.85rem;
        color: #7d8590;
        text-align: center;
        margin-top: 2rem;
        border-top: 1px solid rgba(255,255,255,0.05);
        padding-top: 1rem;
    }

    [direction="rtl"] { text-align: right; }
</style>
""", unsafe_allow_html=True)

# --- API CONFIGURATION ---
API_KEY = "AIzaSyCyAiHiHwNA9oUtmXxvM172Wr2oeyEknpQ"
genai.configure(api_key=API_KEY)

# --- SYSTEM PROMPT ---
SYSTEM_PROMPT = """
You are 'Omar AI', an elite general-purpose assistant.
DEVELOPER IDENTITY:
- You were developed by the visionary AI Engineer: Omar Al-Shawsh (عمر الشاوش).
- Bio: Omar is a brilliant student at Al-Razi University (level 1) and a formidable rising power in Artificial Intelligence. He is dedicated to excellence in Machine Learning and Computer Vision.
- Represent him with great respect and professional pride.

CAPABILITIES:
- You are an expert in science, technology, programming, health, history, and general guidance.
- Respond with creative, accurate, and detailed information.
- Use a professional yet helpful tone.
"""

# --- INITIALIZE MODEL ---
model = genai.GenerativeModel(
    model_name="gemini-flash-latest",
    system_instruction=SYSTEM_PROMPT
)

# --- SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>🚀 Omar AI</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    if st.button("✨ New Chat | محادثة جديدة", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("### Profile")
    st.write("**Developer:** Omar Al-Shawsh")
    st.write("**Mode:** Universal Assistant")
    
    st.markdown("---")
    st.info("I am 'Omar AI', your assistant in all fields.")

# --- MAIN UI ---
st.markdown("""
<div style='text-align: center; margin-bottom: 2rem;'>
    <h1 style='margin-bottom: 0;'>Omar AI 🚀</h1>
    <p style='color: #888;'>Powered by Omar Al-Shawsh Intelligence | مدعوم بذكاء عمر الشاوش</p>
</div>
""", unsafe_allow_html=True)

# Display Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Message Omar AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_text = ""
        try:
            chat = model.start_chat(history=[
                {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]} 
                for m in st.session_state.messages[:-1]
            ])
            response = chat.send_message(prompt, stream=True)
            for chunk in response:
                full_text += chunk.text
                placeholder.markdown(full_text + " ❇️")
            placeholder.markdown(full_text)
            st.session_state.messages.append({"role": "assistant", "content": full_text})
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("<div class='footer-note'>🚀 Omar AI Analysis Complete | Developed by Omar Al-Shawsh.</div>", unsafe_allow_html=True)