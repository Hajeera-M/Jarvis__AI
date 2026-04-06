"""
JARVIS-X — Web Search Tool
Uses DuckDuckGo for free web search.
"""

from duckduckgo_search import DDGS


async def search(query: str, max_results: int = 5) -> str:
    """
    Search the web using DuckDuckGo.
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return
    
    Returns:
        Formatted string of search results
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))

        if not results:
            return f"No results found for: {query}"

        formatted = []
        for i, r in enumerate(results, 1):
            title = r.get("title", "No title")
            body = r.get("body", "No description")
            url = r.get("href", "")
            formatted.append(f"{i}. {title}\n   {body}\n   URL: {url}")

        return "\n\n".join(formatted)

    except Exception as e:
        return f"Search error: {str(e)}"
