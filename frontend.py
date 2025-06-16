import streamlit as st
import requests

# Page setup
st.set_page_config(page_title="Agentic AI Chatbot 🤖", layout="centered")
st.markdown("<h1 style='text-align: center;'>🤖 Agentic AI Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Chat with a smart assistant powered by LLMs + Tools!</p>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar configuration
with st.sidebar:
    st.markdown("### ⚙️ Configuration", unsafe_allow_html=True)
    model_name = st.selectbox("Select Model", ["llama3-70b-8192", "mixtral-8x-7b-32768", "llama-3.3-70b-versatile"])
    model_provider = st.selectbox("Select Provider", ["groq", "openai", "any"])
    system_prompt = st.text_area(
        "System Prompt",
        "You are a smart and friendly AI assistant. Use the DuckDuckGo search tool only when strictly necessary.",
        height=120
    )
    allow_search = st.checkbox("🔍 Allow DuckDuckGo Search", value=True)
    st.markdown("---")
    st.info("You can modify system behavior and model above.")

# Initialize message state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for role, content in st.session_state.messages:
    with st.chat_message(role):
        st.markdown(f"**{role.capitalize()}**: {content}", unsafe_allow_html=True)

# User input box
user_input = st.chat_input("Type your message...")

if user_input:
    # Display user message
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append(("user", user_input))

    payload = {
        "model_name": model_name,
        "model_provider": model_provider,
        "system_prompt": system_prompt,
        "messages": [msg[1] for msg in st.session_state.messages if msg[0] == "user"],
        "allow_search": allow_search
    }

    with st.spinner("🤖 Thinking..."):
        try:
            response = requests.post("http://127.0.0.1:8000/chat", json=payload)
            response.raise_for_status()

            result = response.json()
            ai_response = result.get("response", "🤷 No response from model.")
            st.chat_message("assistant").markdown(ai_response)
            st.session_state.messages.append(("assistant", ai_response))

        except Exception as e:
            st.error(f"❌ Error: {e}")
