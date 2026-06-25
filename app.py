import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime
from groq import Groq
from dotenv import load_dotenv

# ================= LOAD ENV =================
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

# ================= CONFIG =================
st.set_page_config(page_title="Student Assist Chatbot", page_icon="", layout="centered")

ADMIN_PASSWORD = "admin123"
LOG_FOLDER = "chatlogs"
os.makedirs(LOG_FOLDER, exist_ok=True)

# ================= SESSION STATE =================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ================= LOAD INTENTS =================
def load_intents():
    with open("intents.json", "r", encoding="utf-8") as f:
        return json.load(f)

def get_intent_response(user_input):
    data = load_intents()

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            if pattern.lower() in user_input.lower():
                return intent["responses"][0]
    return None

# ================= GROQ AI RESPONSE =================
def get_ai_response(user_input):

    system_prompt = """
    You are a helpful College AI Assistant chatbot.
    Answer student questions in simple and short way.
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )

    return response.choices[0].message.content

# ================= HEADER =================
st.title(" Student Assist Chatbot")

mode = st.sidebar.selectbox("Select Mode", ["Student", "Admin"])

# ================= ADMIN PANEL =================
if mode == "Admin":
    password = st.sidebar.text_input("Enter Admin Password", type="password")

    if password != ADMIN_PASSWORD:
        st.warning("Wrong password ")
        st.stop()

    st.subheader(" Admin Dashboard")

    files = os.listdir(LOG_FOLDER)

    if not files:
        st.info("No chat logs found.")
        st.stop()

    for file in files:
        st.write(f"👤 {file.replace('.csv','')}")
        df = pd.read_csv(os.path.join(LOG_FOLDER, file))
        st.dataframe(df)

    st.stop()

# ================= STUDENT =================
student_name = st.text_input(" Enter your name")

if student_name:
    file_path = os.path.join(LOG_FOLDER, f"{student_name}.csv")

    if not os.path.exists(file_path):
        pd.DataFrame(columns=["time", "user", "bot"]).to_csv(file_path, index=False)

# ================= CHAT INPUT =================
if student_name:

    user_input = st.chat_input("Ask your question...")

    if user_input:

        # Save user message
        st.session_state.messages.append(("user", user_input))

        # STEP 1: INTENTS CHECK
        reply = get_intent_response(user_input)

        # STEP 2: AI FALLBACK
        if not reply:
            reply = get_ai_response(user_input)

        st.session_state.messages.append(("assistant", reply))

        # SAVE TO CSV
        df = pd.read_csv(file_path)

        new_row = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user": user_input,
            "bot": reply
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(file_path, index=False)

# ================= CHAT DISPLAY =================
for role, msg in st.session_state.messages:
    with st.chat_message(role):
        st.write(msg)