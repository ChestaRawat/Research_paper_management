# ============================================================
# PAGE: CITATION ANALYSIS
# ============================================================
# This page visualizes the citation structure of the paper.
#
# Features:
#   - List of all extracted references
#   - Simple citation count chart
#   - Google Scholar search links for each reference
#   - Basic citation relationship display
#
# NOTE FOR BEGINNERS:
# A full citation graph (showing how papers cite each other)
# would require a database like Semantic Scholar's API.
# Here we show the simpler version: references extracted from
# the paper itself, which is a great starting point.
# ============================================================

import streamlit as st

st.set_page_config(page_title="Citation Analysis", page_icon="🔗", layout="wide")
st.title("🔗 Citation Analysis")
st.markdown("Explore the references and citations in your research paper.")

# ============================================================
# CHECK IF PAPER IS LOADED
# ============================================================

metadata = st.session_state.get("paper_metadata", None)

if not metadata:
    st.warning("⚠️ No paper loaded yet.")
    st.info("👈 Go to the **Main Page** and upload a research paper first.")
    st.stop()

paper_title = metadata.get("title", "This Paper")
references  = metadata.get("references", [])

# ============================================================
# SUMMARY STATS
# ============================================================

st.subheader("📊 Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Paper Title", paper_title[:40] + "..." if len(paper_title) > 40 else paper_title)

with col2:
    st.metric("References Found", len(references))

with col3:
    year = metadata.get("year", "Unknown")
    st.metric("Published Year", year)


# ============================================================
# REFERENCES TABLE
# ============================================================
# Display all extracted references in a clean table format.
# ============================================================

st.markdown("---")
st.subheader("📚 Referenced Papers")

if not references:
    st.info("No references were extracted from this paper.")
    st.markdown("""
    **Why might this happen?**
    - The PDF might use a non-standard reference format
    - The references section might not be at the start of the document
    - Try uploading a paper with a clear "References" section
    """)

else:
    # Create a table-like display
    for i, ref in enumerate(references, start=1):

        col_num, col_ref, col_link = st.columns([0.5, 7, 2])

        with col_num:
            st.markdown(f"**{i}**")

        with col_ref:
            st.write(ref)

        with col_link:
            # Generate Google Scholar URL for this reference
            scholar_url = f"https://scholar.google.com/scholar?q={ref.replace(' ', '+').replace(',', '')}"
            st.markdown(f"[🔍 Scholar]({scholar_url})")

    st.markdown("---")

    # --------------------------------------------------------
    # SIMPLE VISUALIZATION
    # --------------------------------------------------------
    # Show reference count as a simple progress-style display.
    # --------------------------------------------------------
    st.subheader("📈 Reference Analysis")

    st.info(f"""
    This paper cites **{len(references)} papers** (extracted from the document).

    **What this means:**
    - Higher citation count → builds on a larger body of prior work
    - Papers in AI/ML typically cite 20-50+ references
    - Fewer references may indicate a shorter or survey-style abstract
    """)

    # If we have enough references, show a word frequency chart
    if len(references) >= 3:
        st.markdown("**Reference Length Distribution:**")

        # Show a basic bar-like display using Streamlit progress bars
        for ref in references[:10]:  # Show max 10
            word_count = len(ref.split())
            # Normalize to 0-100 scale for progress bar
            normalized = min(word_count * 5, 100)
            st.markdown(f"*{ref[:60]}...*" if len(ref) > 60 else f"*{ref}*")
            st.progress(normalized / 100)