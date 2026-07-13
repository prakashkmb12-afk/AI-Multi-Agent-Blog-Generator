import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load environment variables from .env file
load_dotenv()

def get_groq_llm(model_name: str = None, temperature: float = None) -> ChatGroq:
    """
    Initializes and returns a ChatGroq LLM instance.
    Checks environment variables 'GROQ_MODEL_NAME' and 'GROQ_TEMPERATURE' first.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables. Please check your .env file.")
    
    # Read from environment variables if not provided as argument
    if model_name is None:
        model_name = os.getenv("GROQ_MODEL_NAME", "llama-3.1-8b-instant")
    if temperature is None:
        try:
            temperature = float(os.getenv("GROQ_TEMPERATURE", "0.7"))
        except ValueError:
            temperature = 0.7
            
    return ChatGroq(
        api_key=api_key,
        model=model_name,
        temperature=temperature
    )
