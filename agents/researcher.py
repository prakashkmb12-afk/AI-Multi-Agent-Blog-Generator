from state.agent_state import AgentState
from tools.search_tool import search_web

def researcher_node(state: AgentState) -> dict:
    """
    Researcher Agent Node.
    Reads the topic from the state, searches the web, and returns the updated research data.
    """
    topic = state.get("topic")
    print(f"\n[Researcher Agent] Searching the web for info on: '{topic}'...")
    
    # Perform search using our search tool wrapper
    search_results = search_web(topic, max_results=5)
    
    print("[Researcher Agent] Research gathered and saved to shared state.")
    return {"research_data": search_results}
