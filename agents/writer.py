from state.agent_state import AgentState
from config.groq_config import get_groq_llm
from prompts.writer_prompt import WRITER_PROMPT

def writer_node(state: AgentState) -> dict:
    """
    Writer Agent Node.
    Reads topic and research_data, uses the prompt template to call ChatGroq,
    and returns the generated blog post.
    """
    topic = state.get("topic")
    research_data = state.get("research_data")
    
    print(f"\n[Writer Agent] Generating blog post for: '{topic}' using Llama 3 via Groq...")
    
    # Instantiate ChatGroq model
    llm = get_groq_llm()
    
    # Format the prompt template
    formatted_prompt = WRITER_PROMPT.format(topic=topic, research_data=research_data)
    
    # Get response from the model
    response = llm.invoke(formatted_prompt)
    
    print("[Writer Agent] Blog post generated and saved to shared state.")
    return {"blog_post": response.content}
