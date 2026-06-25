#  Student Assist Chatbot

A smart AI-powered **college assistant chatbot** built using **Python, Streamlit, and Groq API**.  
It answers student queries, uses predefined intents, and stores chat history for each user.

---

##  Live Demo
https://studentassistantchatbot-3i7iefkio6ydjeajbe3h2u.streamlit.app/


---

##  Features

- User friendly chat interface
-  College FAQ support using `intents.json`
-  AI responses using Groq LLM API
-  Separate chat history for each student
-  Admin dashboard to view student chats
-  Secure API key using Streamlit Secrets
-  Chat logs stored per user
-  Fully deployed on Streamlit Cloud

---

##  Tech Stack

- Python 
- Streamlit 
- Groq API 
- Pandas 
- JSON (intents system)

---
## How It Works

Student enters name
Types question in chat
System checks:
First → intents.json
Else → Groq AI response
Response is displayed in UI
Chat is saved in CSV logs

## Admin Panel

Login using admin password
View all student chat history
Monitor queries per student


