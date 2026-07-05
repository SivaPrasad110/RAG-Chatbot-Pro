import streamlit as st
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer
from openai import OpenAI

from config import (
    GROQ_API_KEY,
    GROQ_MODEL
)

# =====================================================
# GROQ CLIENT
# =====================================================

client = OpenAI(

    api_key=GROQ_API_KEY,

    base_url="https://api.groq.com/openai/v1"

)

# =====================================================
# LOAD EMBEDDING MODEL
# =====================================================

@st.cache_resource
def load_embedding_model():

    """
    Load SentenceTransformer only once.
    """

    return SentenceTransformer(

        "all-MiniLM-L6-v2"

    )

# Global embedding model

embedding_model = load_embedding_model()

# =====================================================
# EMBED QUESTION
# =====================================================

def embed_question(question):

    """
    Convert question into embedding.
    """

    embedding = embedding_model.encode(

        [question],

        convert_to_numpy=True

    )

    embedding = embedding.astype("float32")

    # Normalize for cosine similarity

    faiss.normalize_L2(embedding)

    return embedding
