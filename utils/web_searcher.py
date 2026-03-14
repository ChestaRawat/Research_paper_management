from tavily import TavilyClient


def web_search(query: str, api_key: str, max_results: int = 3) -> str:

    try:
        tavily = TavilyClient(api_key=api_key)

        results = tavily.search(
            query=query,
            max_results=max_results
        )

        formatted_results = []

        for i, result in enumerate(results.get("results", []), start=1):
            title   = result.get("title", "Untitled")
            content = result.get("content", "No content available")
            url     = result.get("url", "No URL")

            formatted_results.append(
                f"**Result {i}: {title}**\n{content}\n🔗 Source: {url}"
            )

        if formatted_results:
            return "\n\n---\n\n".join(formatted_results)
        else:
            return "No results found for this query."

    except Exception as e:
        print(f"Web search error: {e}")
        return f"Web search failed. Error: {str(e)}"