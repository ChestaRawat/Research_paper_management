# 📚 Research Paper Management & Analysis Intelligence System

An AI-powered research assistant that helps you upload academic papers, extract insights, summarize content, and perform intelligent question-answering using **LLMs + RAG (Retrieval-Augmented Generation)**.

---

## 🚀 Features

| Feature | Description |
|---|---|
| 📄 Paper Upload | Upload PDF or TXT research papers |
| 🧠 Metadata Extraction | Auto-extract title, authors, abstract, year, keywords |
| 🔍 Semantic Q&A | Ask questions — AI finds and answers from the paper |
| 🌐 Web Search Fallback | If answer not in paper, searches the web via Tavily |
| 📝 Structured Summaries | Problem, approach, results, limitations |
| 🔗 Citation Analysis | View and explore all cited references |
| 💬 Research Chat | Dedicated chat interface with history |

---

## 🧠 How RAG Works (Beginner Explanation)

```
User uploads paper → Split into chunks → Convert to vectors → Store in FAISS
                                                                      ↓
User asks a question → Question converted to vector → Find similar chunks
                                                                      ↓
                              Relevant chunks + Question → Send to Gemini LLM
                                                                      ↓
                                                         LLM generates answer
```

**Why not just send the full paper to the LLM?**
- Papers can be 20-30 pages → too many tokens
- RAG retrieves ONLY the relevant parts → faster, cheaper, more accurate

---

## 🗂️ Project Structure

```
ResearchPaperSystem/
│
├── app.py                      # Main page (upload + Q&A + summary)
│
├── pages/
│   ├── 1_Paper_Insights.py     # Metadata display + references
│   ├── 2_Research_Chat.py      # Dedicated chat interface
│   └── 3_Citation_Analysis.py  # Citation visualization
│
├── utils/
│   ├── __init__.py             # Makes utils a Python package
│   ├── document_processor.py   # Load + split documents
│   ├── metadata_extractor.py   # Extract title, authors, etc.
│   ├── embeddings_store.py     # Build FAISS vector database
│   ├── rag_engine.py           # RAG pipeline (retrieve + generate)
│   ├── web_searcher.py         # Tavily web search
│   └── summarizer.py           # Paper summarization
│
├── requirements.txt            # All Python dependencies
├── .env.example                # Template for API keys
├── .env                        # Your actual API keys (NOT on GitHub)
├── .gitignore                  # Files excluded from git
└── README.md
```

---

## ⚙️ Installation & Setup

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/ResearchPaperSystem.git
cd ResearchPaperSystem
```

### Step 2: Create a Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Add Your API Keys

Create a `.env` file in the project root:
```
GEMINI_API_KEY=your_gemini_api_key_here
TAVILY_KEY=your_tavily_api_key_here
```

**Where to get the keys:**
- **Gemini API Key** → https://aistudio.google.com/app/apikey (Free tier available)
- **Tavily API Key** → https://app.tavily.com/ (Free tier: 1000 searches/month)

### Step 5: Run the App
```bash
streamlit run app.py
```

Open your browser at: `http://localhost:8501`

---

## 🧩 Tech Stack

| Technology | Purpose |
|---|---|
| **Streamlit** | Web UI framework |
| **Google Gemini** | LLM for text generation + embeddings |
| **LangChain** | Document loading, text splitting |
| **FAISS** | Vector database for semantic search |
| **Tavily** | Real-time web search API |
| **PyPDF** | PDF text extraction |
| **Python dotenv** | Managing API keys via .env |

---

## 📖 Pages Guide

### Page 1: Main App (`app.py`)
- Upload your research paper
- Ask questions (RAG or web search)
- Generate structured summary

### Page 2: Paper Insights (`pages/1_Paper_Insights.py`)
- View extracted metadata
- See keywords as visual badges
- Quick 5-bullet summary

### Page 3: Research Chat (`pages/2_Research_Chat.py`)
- Full chat interface
- Example questions to get started
- Chat history within the session

### Page 4: Citation Analysis (`pages/3_Citation_Analysis.py`)
- All referenced papers listed
- Google Scholar links for each reference
- Reference count statistics

---

## 🔒 Environment Variables

| Variable | Description | Where to get |
|---|---|---|
| `GEMINI_API_KEY` | Google Gemini LLM + Embeddings | aistudio.google.com |
| `TAVILY_KEY` | Web search fallback | app.tavily.com |

---

## 💡 Example Questions to Ask

- "What problem does this paper solve?"
- "What datasets were used for evaluation?"
- "What is the proposed architecture?"
- "How does this compare to previous methods?"
- "What are the main limitations of this work?"
- "What future work is suggested?"

---

## 🔮 Future Improvements

- [ ] Multi-paper comparison across documents
- [ ] Export summaries to PDF or Word
- [ ] Citation network graph visualization
- [ ] Research trend analysis across multiple papers
- [ ] User notes and highlights system
- [ ] Semantic Scholar API integration for citation counts

---

## 👨‍💻 Author

Built as a portfolio project demonstrating:
- Retrieval-Augmented Generation (RAG)
- LLM orchestration with LangChain
- Vector search with FAISS
- Multi-page Streamlit applications
