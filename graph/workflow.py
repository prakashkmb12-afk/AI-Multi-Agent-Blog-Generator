from langgraph.graph import StateGraph, END
from state.agent_state import AgentState
from agents.researcher import researcher_node
from agents.writer import writer_node

def create_workflow():
    """
    Creates and compiles the LangGraph StateGraph containing:
    1. Researcher Agent Node (first step)
    2. Writer Agent Node (second step)
    """
    # Initialize StateGraph with the shared state structure
    workflow = StateGraph(AgentState)
    
    # Register the nodes
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("writer", writer_node)
    
    # Set entry point
    workflow.set_entry_point("researcher")
    
    # Connect nodes in sequence
    workflow.add_edge("researcher", "writer")
    workflow.add_edge("writer", END)
    
    # Compile into a runnable application
    return workflow.compile()
