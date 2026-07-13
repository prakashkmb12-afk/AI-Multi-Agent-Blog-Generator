from duckduckgo_search import DDGS

def search_web(query: str, max_results: int = 5) -> list:
    """
    Searches DuckDuckGo for the given query and returns a list of result dictionaries.
    """
    try:
        with DDGS() as ddgs:
            raw_results = list(ddgs.text(query, max_results=max_results))
            if not raw_results:
                return []
            
            results = []
            for r in raw_results:
                results.append({
                    "title": r.get("title", "No Title"),
                    "link": r.get("href", "No Link"),
                    "snippet": r.get("body", "No Description")
                })
            return results
    except Exception as e:
        # Return fallback structured error result
        return [{
            "title": f"Error performing search for query: '{query}'",
            "link": "#",
            "snippet": str(e)
        }]
