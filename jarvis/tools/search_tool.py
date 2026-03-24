"""
JARVIS — Search Tool
Uses duckduckgo-search to perform web queries.
"""

from duckduckgo_search import DDGS

def search_web(query: str, max_results: int = 3) -> str:
    """
    Search the web using DuckDuckGo.
    """
    if not query:
        return "Error: No search query provided."

    print(f"[JARVIS Tool] Searching the web for: {query}")
    try:
        results = DDGS().text(query, max_results=max_results)
        if not results:
            return f"No results found for '{query}'."

        formatted = []
        for i, res in enumerate(results):
            title = res.get('title', 'Unknown Title')
            body = res.get('body', 'No snippet')
            url = res.get('href', '')
            formatted.append(f"Result {i+1}: {title}\nSnippet: {body}\nSource: {url}")

        return "\n\n".join(formatted)
    except Exception as e:
        return f"Web search failed: {e}"
