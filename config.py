import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Choose the Gemini model you want to use
model="gemini-2.0-flash"
