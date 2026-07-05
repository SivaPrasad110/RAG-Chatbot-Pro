import streamlit as st
import numpy as np
import faiss

from sentence_transformers import SentenceTransformer

from google import genai

from config import GEMINI_API_KEY


# ==========================================================
# GEMINI CLIENT
# ==========================================================

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ==========================================================
# LOAD EMBEDDING MODEL
# ==========================================================

@st.cache_resource
def load_embedding_model():

    """
    Load Sentence Transformer only once.
    """

    model = SentenceTransformer(

        "all-MiniLM-L6-v2"

    )

    return model


# ==========================================================
# EMBEDDING MODEL
# ==========================================================

embedding_model = load_embedding_model()


# ==========================================================
# CREATE VECTOR STORE
# ==========================================================

@st.cache_resource(show_spinner=False)
def create_vector_store(chunks):

    """
    Create FAISS Index
    """

    texts = [

        chunk["text"]

        for chunk in chunks

    ]

    embeddings = embedding_model.encode(

        texts,

        convert_to_numpy=True,

        show_progress_bar=False

    )

    embeddings = embeddings.astype("float32")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(

        dimension

    )

    index.add(

        embeddings

    )

    return index


# ==========================================================
# EMBED QUESTION
# ==========================================================

def embed_question(question):

    embedding = embedding_model.encode(

        [question],

        convert_to_numpy=True

    )

    return embedding.astype("float32")
    # ==========================================================
# SEARCH CHUNKS
# ==========================================================

def search_chunks(

    question,

    chunks,

    index,

    top_k=5

):

    """
    Search the FAISS index and return
    the most relevant chunks.
    """

    # ------------------------------------
    # Embed Question
    # ------------------------------------

    query_embedding = embed_question(question)

    # ------------------------------------
    # Search FAISS
    # ------------------------------------

    distances, indices = index.search(

        query_embedding,

        top_k

    )

    results = []

    # ------------------------------------
    # Collect Results
    # ------------------------------------

    for score, idx in zip(

        distances[0],

        indices[0]

    ):

        # Ignore invalid index

        if idx < 0:

            continue

        # Ignore out-of-range index

        if idx >= len(chunks):

            continue

        chunk = chunks[idx]

        # Convert L2 distance into an easy score

        similarity = float(

            1 / (1 + score)

        )

        results.append(

            {

                "text": chunk.get("text", ""),

                "source": chunk.get(

                    "source",

                    "Unknown"

                ),

                "page": chunk.get(

                    "page",

                    "-"

                ),

                "score": round(

                    similarity,

                    3

                )

            }

        )

    return results
from config import GEMINI_MODEL


# ==========================================================
# BUILD PROMPT
# ==========================================================

def build_prompt(question, context):

    prompt = f"""
You are a professional AI assistant.

Your job is to answer ONLY using the provided context.

Rules:

1. Use the document context whenever possible.
2. If the answer is not found in the context, clearly say:
   "I couldn't find this information in the uploaded documents."
3. Do not invent or hallucinate facts.
4. Explain the answer clearly using simple language.
5. Use bullet points when appropriate.
6. If the context contains multiple relevant facts, summarize them.

========================
DOCUMENT CONTEXT
========================

{context}

========================
USER QUESTION
========================

{question}

========================
ANSWER
========================
"""

    return prompt


# ==========================================================
# ASK GEMINI
# ==========================================================

def ask_gemini(question, context):

    try:

        prompt = build_prompt(
            question,
            context
        )

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        if response is None:
            return "❌ No response received from Gemini."

        if not hasattr(response, "text"):
            return "❌ Unable to generate an answer."

        answer = response.text.strip()

        if answer == "":
            return "❌ Gemini returned an empty response."

        return answer

    except Exception as e:

        return f"""
⚠️ Error while contacting Gemini

{str(e)}
"""
