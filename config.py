import os
from dotenv import load_dotenv

# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()

# ==========================================
# GEMINI API KEY
# ==========================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ==========================================
# GEMINI MODEL
# ==========================================

# Option 1 (Recommended if available)
GEMINI_MODEL = "gemini-2.0-flash"

# Option 2 (If 2.0 is unavailable)
# GEMINI_MODEL = "gemini-1.5-flash"
