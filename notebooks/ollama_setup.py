"""
Ollama setup module for LangChain notebooks.

This module handles all Ollama initialization, so you don't need to repeat
the setup code in every notebook. Just import it and you're ready to go.

Usage in notebooks:
    from ollama_setup import llm
    # Now you can use llm directly in your chains and agents
"""

import os
from dotenv import load_dotenv
from langchain_ollama import OllamaLLM

# Load environment variables from .env file
load_dotenv()

# Get Ollama configuration from environment
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

# Initialize the Ollama LLM
llm = OllamaLLM(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=0.7,  # Adjust as needed
)

# Print initialization info (helpful for debugging)
print(f"✅ Ollama LLM initialized")
print(f"   Model: {OLLAMA_MODEL}")
print(f"   Base URL: {OLLAMA_BASE_URL}")
