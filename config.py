import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Choose the Gemini model you want to use
GEMINI_MODEL = "gemini-2.5-flash"
