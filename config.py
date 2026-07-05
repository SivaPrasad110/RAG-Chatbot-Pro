import os
from dotenv import load_dotenv

load_dotenv()

# ==========================================
# GEMINI SETTINGS
# ==========================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Recommended model
GEMINI_MODEL = "gemini-2.0-flash"

# Alternative:
# GEMINI_MODEL = "gemini-1.5-flash"
