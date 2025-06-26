import streamlit as st
import requests

# ------------------------------------
# 💄 Custom CSS for improved layout
# ------------------------------------
st.markdown("""
    <style>
        .chat-message {
            padding: 0.8em;
            border-radius: 1em;
            margin: 0.5em 0;
            max-width: 80%;
            word-wrap: break-word;
        }
        .user-message {
            background-color: #DCF8C6;
            margin-left: auto;
            text-align: right;
        }
        .ai-message {
            background-color: #F1F0F0;
            margin-right: auto;
            text-align: left;
        }
        .stChatInput {
            margin-top: 2em;
        }
        .sidebar-title {
            font-size: 1.2em;
            font-weight: bold;
            margin-bottom: 1em;
        }
    </style>
""", unsafe_allow_html=True)

# ------------------------------------
# 🧾 Page Setup
# ------------------------------------
st.set_page_config(page_title="Agentic AI Chatbot 🤖", layout="centered")
st.markdown("<h1 style='text-align: center;'>🤖 Agentic AI Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Chat with a smart assistant powered by LLMs + Tools!</p>", unsafe_allow_html=True)
st.markdown("---")

# ------------------------------------
# ⚙️ Sidebar Configuration
# ------------------------------------
with st.sidebar:
    st.markdown("<div class='sidebar-title'>⚙️ Configuration</div>", unsafe_allow_html=True)
    model_name = st.selectbox("Select Model", ["llama3-70b-8192", "mixtral-8x-7b-32768", "llama-3.3-70b-versatile"])
    model_provider = st.selectbox("Select Provider", ["groq", "openai", "any"])
    system_prompt = st.text_area(
        "System Prompt",
        "You are a smart and friendly AI assistant. Use the DuckDuckGo search tool only when strictly necessary.",
        height=120
    )
    allow_search = st.checkbox("🔍 Allow DuckDuckGo Search", value=True)
    st.markdown("---")
    st.info("Modify system behavior and model preferences here.")

# ------------------------------------
# 💬 Chat History State
# ------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ------------------------------------
# 🖥️ Chat Message Display
# ------------------------------------
for role, content in st.session_state.messages:
    alignment = "user-message" if role == "user" else "ai-message"
    st.markdown(
        f"<div class='chat-message {alignment}'><strong>{role.capitalize()}:</strong> {content}</div>",
        unsafe_allow_html=True
    )

# ------------------------------------
# 🧑‍💻 Chat Input Section
# ------------------------------------
user_input = st.chat_input("Type your message here...")

if user_input:
    # Store user message
    st.session_state.messages.append(("user", user_input))

    # Payload for backend
    payload = {
        "model_name": model_name,
        "model_provider": model_provider,
        "system_prompt": system_prompt,
        "messages": [msg[1] for msg in st.session_state.messages if msg[0] == "user"],
        "allow_search": allow_search
    }

    # Call backend
    with st.spinner("🤖 Thinking..."):
        try:
            response = requests.post("https://langgraph-chat-agent.onrender.com/chat", json=payload)
            response.raise_for_status()
            result = response.json()
            ai_response = result.get("response", "🤷 No response from model.")

        except Exception as e:
            ai_response = f"❌ Error: {e}"

    # Store and display AI message
    st.session_state.messages.append(("assistant", ai_response))
    st.experimental_rerun()  # Force refresh to update chat layout with aligned bubbles
