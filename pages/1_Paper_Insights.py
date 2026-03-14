import streamlit as st
from dotenv import load_dotenv
import os
from utils.summarizer import quick_summary
from utils.metadata_extractor import format_metadata_display

load_dotenv()
# CHANGED: GOOGLE_API_KEY → MISTRAL_API_KEY
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

st.set_page_config(page_title="Paper Insights", page_icon="📊", layout="wide")
st.title("📊 Paper Insights")

metadata = st.session_state.get("paper_metadata", None)

if not metadata:
    st.warning("⚠️ No paper loaded yet.")
    st.info("👈 Go to the **Main Page** and upload a research paper first.")
    st.stop()

st.header("📄 Paper Information")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Title")
    st.markdown(f"### {metadata['title']}")

    st.subheader("Authors")
    st.write(metadata["authors"])

    st.subheader("Keywords")
    if metadata.get("keywords"):
        keywords = [k.strip() for k in metadata["keywords"].split(",")]
        keyword_html = " ".join([
            f'<span style="background:#1e3a5f;color:white;padding:3px 10px;border-radius:12px;margin:3px;display:inline-block;">{k}</span>'
            for k in keywords if k
        ])
        st.markdown(keyword_html, unsafe_allow_html=True)
    else:
        st.write("Not available")

with col2:
    st.subheader("Published Year")
    year = metadata.get("year", "Unknown")
    st.markdown(f"<h1 style='color:#4CAF50;text-align:center;'>{year}</h1>", unsafe_allow_html=True)

    st.subheader("References Found")
    ref_count = len(metadata.get("references", []))
    st.markdown(f"<h1 style='color:#2196F3;text-align:center;'>{ref_count}</h1>", unsafe_allow_html=True)

st.markdown("---")
st.subheader("📝 Abstract")
abstract = metadata.get("abstract", "Abstract not available.")
st.markdown(f"> {abstract}")

st.markdown("---")
st.subheader("⚡ Quick 5-Point Summary")

if st.button("Generate Quick Summary"):
    with st.spinner("Generating..."):
        # CHANGED: GOOGLE_API_KEY → MISTRAL_API_KEY
        bullet_summary = quick_summary(
            abstract,
            MISTRAL_API_KEY
        )
    st.markdown(bullet_summary)

st.markdown("---")
st.subheader("🔗 Cited References")

references = metadata.get("references", [])

if references:
    st.info(f"Found {len(references)} referenced papers in this document.")

    for i, ref in enumerate(references, start=1):
        with st.expander(f"📄 Reference {i}"):
            st.write(ref)
            search_url = f"https://scholar.google.com/scholar?q={ref.replace(' ', '+')}"
            st.markdown(f"[🔍 Search on Google Scholar]({search_url})")
else:
    st.info("No references were extracted from this paper.")