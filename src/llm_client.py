from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

def get_llm(model_name: str = "llama-3.1-8b-instant"):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY not set")
    return ChatGroq(model=model_name, temperature=0.4, groq_api_key=api_key)
