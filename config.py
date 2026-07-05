import os
from dotenv import load_dotenv

load_dotenv()

# =========================================
# xAI API
# =========================================

XAI_API_KEY = os.getenv("XAI_API_KEY")

# Grok Model
XAI_MODEL = "grok-4"
