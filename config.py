"""
config.py
Configuration Settings
"""

import os
from dotenv import load_dotenv

# Load environment variables (ensure .env in project root is found)
load_dotenv(override=False)

# Gemini API Key
# NOTE: Read from environment variable named GEMINI_API_KEY
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "❌ GEMINI_API_KEY not found. Please create a .env file with GEMINI_API_KEY=" 
        "(or set the environment variable GEMINI_API_KEY)."
    )


# Application Settings

APP_NAME = "Professional RAG Chatbot"

APP_VERSION = "1.0.0"

MAX_FILE_SIZE_MB = 50

DEFAULT_CHUNK_SIZE = 500

DEFAULT_CHUNK_OVERLAP = 100

DEFAULT_TOP_K = 3

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

GEMINI_MODEL = "gemini-2.5-flash"

FAISS_INDEX = "vectorstore/index.faiss"