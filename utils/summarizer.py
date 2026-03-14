from mistralai import Mistral


def summarize_paper(abstract_text: str, api_key: str) -> str:

    client = Mistral(api_key=api_key)

    prompt = f"""
You are an academic paper summarization expert.

Produce a structured summary using this exact format:

## 🎯 Problem Statement
(What problem does this paper address? 2-3 sentences.)

## 💡 Proposed Approach
(What solution or method does the paper propose? 2-3 sentences.)

## ✅ Key Contributions
- Contribution 1
- Contribution 2
- Contribution 3

## 📊 Results
(What were the main findings or results? 2-3 sentences.)

## ⚠️ Limitations
(What are the known limitations or future work? 1-2 sentences.)

If information is not available, write "Not mentioned in abstract."

ABSTRACT TEXT:
{abstract_text[:4000]}
"""

    try:
        response = client.chat.complete(
            model="mistral-small-latest",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating summary: {str(e)}"


def quick_summary(text: str, api_key: str) -> str:

    client = Mistral(api_key=api_key)

    prompt = f"""
Summarize this research paper in exactly 5 bullet points.
Each bullet should be one clear sentence.
Start each bullet with a relevant emoji.

TEXT:
{text[:3000]}
"""

    try:
        response = client.chat.complete(
            model="mistral-small-latest",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"