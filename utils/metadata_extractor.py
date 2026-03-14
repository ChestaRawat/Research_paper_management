import os
from mistralai import Mistral


def extract_metadata_llm(full_text: str, api_key: str) -> dict:

    client = Mistral(api_key=api_key)
    text_sample = full_text[:6000]

    prompt = f"""
You are an academic metadata extraction assistant.

Read the research paper text below and extract the following fields.
Return ONLY in this exact format — no extra explanation:

Title: <paper title>
Authors: <author names separated by commas>
Abstract: <the abstract text, summarized in 2-3 sentences if too long>
Published Year: <year as 4 digits, e.g. 2023>
Keywords: <5-8 keywords separated by commas>
References:
- <reference 1 title>
- <reference 2 title>
- <reference 3 title>
- <reference 4 title>
- <reference 5 title>

Only list references that are actual cited research papers.
If you cannot find a field, write "Not found" for that field.

PAPER TEXT:
{text_sample}
"""

    try:
        response = client.chat.complete(
            model="mistral-small-latest",
            messages=[{"role": "user", "content": prompt}]
        )
        result = response.choices[0].message.content

    except Exception as e:
        print(f"Metadata extraction error: {e}")
        return {
            "title": "Could not extract title",
            "authors": "Unknown",
            "abstract": "Could not extract abstract",
            "year": "Unknown",
            "keywords": "",
            "references": []
        }

    # Parse response line by line
    metadata = {
        "title": "Not found",
        "authors": "Not found",
        "abstract": "Not found",
        "year": "Not found",
        "keywords": "",
        "references": []
    }

    lines = result.strip().split("\n")
    current_section = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        lower_line = line.lower()

        if lower_line.startswith("title:"):
            metadata["title"] = line[len("title:"):].strip()
            current_section = None

        elif lower_line.startswith("authors:"):
            metadata["authors"] = line[len("authors:"):].strip()
            current_section = None

        elif lower_line.startswith("abstract:"):
            metadata["abstract"] = line[len("abstract:"):].strip()
            current_section = None

        elif lower_line.startswith("published year:"):
            metadata["year"] = line[len("published year:"):].strip()
            current_section = None

        elif lower_line.startswith("keywords:"):
            metadata["keywords"] = line[len("keywords:"):].strip()
            current_section = None

        elif lower_line.startswith("references:"):
            current_section = "references"

        elif current_section == "references" and line.startswith("-"):
            ref = line[1:].strip()
            if len(ref) > 10:
                metadata["references"].append(ref)

    return metadata


def format_metadata_display(metadata: dict) -> str:
    output = f"""
**Title:** {metadata.get('title', 'N/A')}
**Authors:** {metadata.get('authors', 'N/A')}
**Year:** {metadata.get('year', 'N/A')}
**Keywords:** {metadata.get('keywords', 'N/A')}
**Abstract:** {metadata.get('abstract', 'N/A')}
"""
    return output