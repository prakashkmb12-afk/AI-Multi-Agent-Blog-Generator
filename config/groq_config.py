import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load environment variables from .env file
load_dotenv()

def get_groq_llm(model_name: str = "llama-3.1-8b-instant", temperature: float = 0.7) -> ChatGroq:
    """
    Initializes and returns a ChatGroq LLM instance.
    Defaults to llama-3.1-8b-instant as it is fast and highly capable.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables. Please check your .env file.")
    
    return ChatGroq(
        api_key=api_key,
        model=model_name,
        temperature=temperature
    )
