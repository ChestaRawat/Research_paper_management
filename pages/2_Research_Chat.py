# ============================================================
# PAGE: RESEARCH CHAT ASSISTANT
# ============================================================
# This page provides a dedicated chat interface for the paper.
#
# Features:
#   - Full chat history with message bubbles
#   - Persistent Q&A within the session
#   - Source citation (paper vs web)
#   - Suggested example questions to help beginners
# ============================================================

import streamlit as st
from dotenv import load_dotenv
import os
from utils.rag_engine import answer_question
from utils.web_searcher import web_search

load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_KEY")

st.set_page_config(page_title="Research Chat", page_icon="💬", layout="wide")
st.title("💬 Research Chat Assistant")
st.markdown("Chat with your research paper using AI.")

# ============================================================
# CHECK IF PAPER IS LOADED
# ============================================================

vector_store = st.session_state.get("vector_store", None)
metadata     = st.session_state.get("paper_metadata", None)

if not vector_store or not metadata:
    st.warning("⚠️ No paper loaded yet.")
    st.info("👈 Go to the **Main Page** and upload a research paper first.")
    st.stop()

st.sidebar.success(f"📄 Paper: {metadata['title'][:50]}...")


# ============================================================
# SESSION STATE FOR CHAT
# ============================================================

if "research_chat_history" not in st.session_state:
    st.session_state.research_chat_history = []


# ============================================================
# EXAMPLE QUESTIONS
# ============================================================
# These help beginners understand what to ask.
# Clicking a question auto-fills the input.
# ============================================================

st.markdown("### 💡 Try asking:")

example_questions = [
    "What problem does this paper solve?",
    "What datasets are used in experiments?",
    "What is the main proposed method?",
    "What are the key results or findings?",
    "What are the limitations of this work?",
    "How does this compare to prior work?"
]

cols = st.columns(3)
selected_example = None

for i, q in enumerate(example_questions):
    if cols[i % 3].button(q, key=f"ex_{i}"):
        selected_example = q


# ============================================================
# CHAT INPUT
# ============================================================

st.markdown("---")

# Pre-fill from example button if clicked
default_query = selected_example if selected_example else ""

user_input = st.text_input(
    "Your question:",
    value=default_query,
    placeholder="Ask anything about the paper...",
    key="chat_input"
)

col1, col2 = st.columns([1, 6])

with col1:
    send_button = st.button("Send 📨", type="primary")

with col2:
    if st.button("🗑️ Clear Chat"):
        st.session_state.research_chat_history = []
        st.rerun()


# ============================================================
# PROCESS THE QUESTION
# ============================================================

if send_button and user_input and len(user_input.strip()) > 3:

    with st.spinner("🤔 Thinking..."):
        answer, source_type = answer_question(
            user_input,
            vector_store,
            MISTRAL_API_KEY,
            TAVILY_API_KEY
        )

    source_label = "📄 Paper" if source_type == "document" else "🌐 Web"

    # Add to chat history
    st.session_state.research_chat_history.append({
        "role": "user",
        "content": user_input
    })
    st.session_state.research_chat_history.append({
        "role": "assistant",
        "content": answer,
        "source": source_label
    })


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================
# We display messages like a chat interface.
# User messages appear on the right, AI on the left.
# ============================================================

st.markdown("---")
st.subheader("📜 Conversation")

if not st.session_state.research_chat_history:
    st.info("Ask a question above to start chatting with your paper!")

else:
    # Display in reverse order (newest first)
    history = st.session_state.research_chat_history

    # Show messages in pairs (user + assistant)
    for i in range(len(history) - 1, -1, -1):
        msg = history[i]

        if msg["role"] == "user":
            # User message — styled differently
            st.markdown(
                f"""<div style='background:#1e3a5f;padding:10px 15px;border-radius:10px;
                margin:5px 0;text-align:right;color:white;'>
                🧑 <b>You:</b> {msg['content']}
                </div>""",
                unsafe_allow_html=True
            )

        elif msg["role"] == "assistant":
            # AI response with source tag
            source = msg.get("source", "")
            st.markdown(
                f"""<div style='background:#2d2d2d;padding:10px 15px;border-radius:10px;
                margin:5px 0;color:#f0f0f0;border-left:4px solid #4CAF50;'>
                🤖 <b>Assistant</b> <small>({source})</small><br><br>{msg['content']}
                </div>""",
                unsafe_allow_html=True
            )