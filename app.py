# ============================================================
# RESEARCH PAPER MANAGEMENT & ANALYSIS INTELLIGENCE SYSTEM
# ============================================================
# Main entry point for the Streamlit application.
# This is the first page the user sees — it handles:
#   - Paper upload (PDF or TXT)
#   - Loading paper from a URL
#   - Asking questions (RAG or Web Search)
#   - Summary generation
# ============================================================

import streamlit as st
from dotenv import load_dotenv
import os

# Import our helper functions from the utils folder
from utils.document_processor import load_document, split_documents, extract_text
from utils.metadata_extractor import extract_metadata_llm
from utils.embeddings_store import build_vector_store
from utils.rag_engine import answer_question
from utils.web_searcher import web_search
from utils.summarizer import summarize_paper

# ============================================================
# STEP 1: LOAD ENVIRONMENT VARIABLES
# ------------------------------------------------------------
# We store API keys in a .env file (not pushed to GitHub).
# load_dotenv() reads that file and makes keys available
# via os.getenv().
# ============================================================
load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


# ============================================================
# STEP 2: CONFIGURE STREAMLIT PAGE
# ============================================================
st.set_page_config(
    page_title="Research Intelligence System",
    page_icon="📚",
    layout="wide"
)

# ============================================================
# STEP 3: SESSION STATE INITIALIZATION
# ------------------------------------------------------------
# Streamlit re-runs the entire script on every user action.
# st.session_state lets us REMEMBER data between re-runs.
#
# We store:
#   - vector_store     → the FAISS database with paper chunks
#   - paper_metadata   → title, authors, abstract, etc.
#   - documents_loaded → flag so we don't reload the same paper
#   - chat_history     → list of questions and answers
# ============================================================
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "paper_metadata" not in st.session_state:
    st.session_state.paper_metadata = None

if "documents_loaded" not in st.session_state:
    st.session_state.documents_loaded = False

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ============================================================
# PAGE HEADER
# ============================================================
st.title("📚 Research Paper Management & Analysis Intelligence System")
st.markdown("Upload a research paper, ask questions, and get AI-powered insights.")
st.divider()


# ============================================================
# SIDEBAR — Global Controls
# ============================================================
st.sidebar.title("⚙️ Controls")
web_toggle = st.sidebar.toggle("🌐 Enable Real-Time Web Search")
st.sidebar.markdown("---")

# Show current paper info in sidebar if loaded
if st.session_state.documents_loaded and st.session_state.paper_metadata:
    meta = st.session_state.paper_metadata
    st.sidebar.success("✅ Paper Loaded")
    st.sidebar.markdown(f"**Title:** {meta['title'][:60]}...")
    st.sidebar.markdown(f"**Year:** {meta['year']}")
    st.sidebar.markdown(f"**Authors:** {meta['authors'][:50]}...")

    # Button to clear and load a new paper
    if st.sidebar.button("🔄 Load New Paper"):
        st.session_state.vector_store = None
        st.session_state.paper_metadata = None
        st.session_state.documents_loaded = False
        st.session_state.chat_history = []
        st.rerun()


# ============================================================
# SECTION A: PAPER UPLOAD
# ------------------------------------------------------------
# We show the upload area only if no paper is loaded yet.
# Once a paper is loaded, we hide the upload area to avoid
# accidental re-loading.
# ============================================================
if not st.session_state.documents_loaded:

    st.header("📄 Step 1: Upload Your Research Paper")

    col1, col2 = st.columns(2)

    with col1:
        uploaded_file = st.file_uploader(
            "Upload a PDF or TXT file",
            type=["pdf", "txt"],
            help="Supports arXiv papers, journal papers, conference papers"
        )

    with col2:
        url_input = st.text_input(
            "Or paste a paper URL",
            placeholder="https://arxiv.org/abs/...",
            help="Paste a direct link to an online research paper"
        )

    st.markdown("---")

    # --------------------------------------------------------
    # DOCUMENT PROCESSING PIPELINE
    # --------------------------------------------------------
    # This triggers when a file is uploaded OR a URL is given.
    #
    # Pipeline steps:
    #   1. Load the document using LangChain loaders
    #   2. Extract raw text (for metadata + summarization)
    #   3. Extract metadata using Gemini LLM
    #   4. Split text into overlapping chunks
    #   5. Generate embeddings for each chunk
    #   6. Store embeddings in FAISS vector database
    # --------------------------------------------------------

    if (uploaded_file or url_input):

        with st.spinner("🔄 Processing your research paper... This may take a moment."):

            # Step 1: Load
            documents = load_document(uploaded_file, url_input)

            if documents:

                # Step 2: Extract full raw text
                raw_text = extract_text(documents)

                # Step 3: Extract structured metadata using LLM
                st.info("🧠 Extracting metadata with AI...")
                metadata = extract_metadata_llm(raw_text, MISTRAL_API_KEY)
                st.session_state.paper_metadata = metadata

                # Step 4: Split into chunks
                chunks = split_documents(documents)

                # Step 5 & 6: Embed chunks and store in FAISS
                st.info("⚡ Building vector database...")
                vector_store = build_vector_store(chunks, MISTRAL_API_KEY)

                if vector_store:
                    st.session_state.vector_store = vector_store
                    st.session_state.documents_loaded = True
                    st.success("✅ Paper loaded successfully! You can now ask questions.")
                    st.rerun()
                else:
                    st.error("❌ Failed to build vector store. Check your API key.")
            else:
                st.error("❌ Could not load the document. Please try a different file.")

else:
    # --------------------------------------------------------
    # PAPER IS ALREADY LOADED — Show confirmation
    # --------------------------------------------------------
    meta = st.session_state.paper_metadata
    st.success(f"📄 **Loaded:** {meta['title']}")


# ============================================================
# SECTION B: QUESTION & ANSWER (RAG PIPELINE)
# ------------------------------------------------------------
# Users type a question in natural language.
#
# Two modes:
# 1. Web Search mode → real-time Tavily search
# 2. RAG mode → retrieve from paper, LLM generates answer
#
# The answer and source are displayed, and the Q&A is
# saved to chat_history for the session.
# ============================================================

st.header("💬 Step 2: Ask a Question")

query = st.text_input(
    "Ask anything about the research paper",
    placeholder="e.g. What problem does this paper solve? What dataset was used?",
    key="main_query"
)

col_ask, col_clear = st.columns([1, 5])

with col_ask:
    ask_button = st.button("🔍 Get Answer", type="primary")

with col_clear:
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()


if ask_button and query and len(query.strip()) > 3:

    # MODE 1: Web Search (user toggled ON)
    if web_toggle:
        with st.spinner("🌐 Searching the web..."):
            answer = web_search(query, TAVILY_API_KEY)
        source = "🌐 Web"

    # MODE 2: RAG from paper
    else:
        if not st.session_state.vector_store:
            st.warning("⚠️ Please upload a paper first before asking questions.")
            st.stop()

        with st.spinner("🧠 Searching paper and generating answer..."):
            answer, source_type = answer_question(
                query,
                st.session_state.vector_store,
                MISTRAL_API_KEY,
                TAVILY_API_KEY
            )

        source = "📄 Research Paper" if source_type == "document" else "🌐 Web (fallback)"

    # Save to chat history
    st.session_state.chat_history.append({
        "question": query,
        "answer": answer,
        "source": source
    })


# ============================================================
# DISPLAY CHAT HISTORY
# ------------------------------------------------------------
# Show all Q&A pairs from this session in a chat-like format.
# Newest questions appear at the top.
# ============================================================

if st.session_state.chat_history:
    st.markdown("---")
    st.subheader("🗂️ Chat History")

    for i, item in enumerate(reversed(st.session_state.chat_history)):
        with st.expander(f"Q: {item['question']}", expanded=(i == 0)):
            st.markdown(f"**Answer:**\n\n{item['answer']}")
            st.caption(f"Source: {item['source']}")


# ============================================================
# SECTION C: PAPER SUMMARIZATION
# ============================================================

st.markdown("---")
st.header("📝 Step 3: Generate Paper Summary")

if st.button("✨ Generate Summary", type="secondary"):

    if not st.session_state.paper_metadata:
        st.warning("⚠️ Please upload a research paper first.")
    else:
        with st.spinner("📝 Generating structured summary..."):
            summary = summarize_paper(
                st.session_state.paper_metadata["abstract"],
                MISTRAL_API_KEY
            )
        st.subheader("Paper Summary")
        st.markdown(summary)