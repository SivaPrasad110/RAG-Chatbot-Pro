import streamlit as st
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

from openai import OpenAI

from config import (
    XAI_API_KEY,
    XAI_MODEL
)

# =====================================================
# xAI CLIENT
# =====================================================

client = OpenAI(

    api_key=XAI_API_KEY,

    base_url="https://api.x.ai/v1"

)

# =====================================================
# LOAD EMBEDDING MODEL
# =====================================================

@st.cache_resource
def load_embedding_model():

    """
    Load Sentence Transformer only once.
    """

    return SentenceTransformer(

        "all-MiniLM-L6-v2"

    )

embedding_model = load_embedding_model()

# =====================================================
# EMBED QUESTION
# =====================================================

def embed_question(question):

    embedding = embedding_model.encode(

        [question],

        convert_to_numpy=True

    )

    return embedding.astype("float32")
