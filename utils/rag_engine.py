import os
from mistralai import Mistral
from utils.embeddings_store import semantic_search
from utils.web_searcher import web_search


def answer_question(query: str, vector_store, api_key: str, tavily_key: str):

    relevant_docs = semantic_search(query, vector_store, top_k=4)
    context = "\n\n---\n\n".join([doc.page_content for doc in relevant_docs])

    client = Mistral(api_key=api_key)

    prompt = f"""
You are a research paper assistant. Answer questions using ONLY the context below.

RULES:
1. Use ONLY the information in the context.
2. Do NOT use your general knowledge.
3. If the answer is NOT in the context, respond with exactly: NOT_FOUND
4. Keep answers clear and concise (3-5 sentences).
5. If quoting from the paper, use quotation marks.

CONTEXT FROM PAPER:
{context}

USER QUESTION:
{query}

ANSWER:
"""

    try:
        response = client.chat.complete(
            model="mistral-small-latest",
            messages=[{"role": "user", "content": prompt}]
        )
        answer = response.choices[0].message.content.strip()

    except Exception as e:
        print(f"LLM error: {e}")
        return f"Error generating answer: {str(e)}", "error"

    if "NOT_FOUND" in answer.upper():
        print("Answer not found in paper — falling back to web search.")
        web_answer = web_search(query, tavily_key)
        return web_answer, "web"

    return answer, "document"