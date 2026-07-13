from duckduckgo_search import DDGS

def search_web(query: str, max_results: int = 5) -> str:
    """
    Searches DuckDuckGo for the given query and returns a formatted string of results.
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
            if not results:
                return f"No search results found for query: '{query}'."
            
            formatted_results = []
            for r in results:
                title = r.get("title", "No Title")
                href = r.get("href", "No Link")
                body = r.get("body", "No Description")
                formatted_results.append(f"Title: {title}\nLink: {href}\nSnippet: {body}\n---")
            return "\n\n".join(formatted_results)
    except Exception as e:
        # Fallback message in case of network/rate-limit issues
        return f"Error performing search for query '{query}': {str(e)}"
