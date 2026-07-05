"""
rag.py
Professional RAG Engine
"""

import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

from google import genai

from config import GEMINI_API_KEY

# ----------------------------------------
# Configure Gemini
# ----------------------------------------

client = genai.Client(
    api_key=GEMINI_API_KEY
)

# ----------------------------------------
# Embedding Model
# ----------------------------------------

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# ----------------------------------------
# Create Vector Store
# ----------------------------------------


def create_vector_store(chunks):

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = embedding_model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    embeddings = embeddings.astype("float32")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(
        dimension
    )

    index.add(
        embeddings
    )

    return index


# ----------------------------------------
# Search Chunks
# ----------------------------------------


def search_chunks(
    question,
    chunks,
    index,
    top_k=3
):

    question_embedding = embedding_model.encode(
        [question],
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    question_embedding = question_embedding.astype(
        "float32"
    )

    scores, indices = index.search(
        question_embedding,
        top_k
    )

    results = []

    for score, idx in zip(
        scores[0],
        indices[0]
    ):

        if idx < len(chunks):

            results.append(

                {
                    "text": chunks[idx]["text"],

                    "source": chunks[idx]["source"],

                    "page": chunks[idx]["page"],

                    "score": float(score)

                }

            )

    return results


# ----------------------------------------
# Build Prompt
# ----------------------------------------


def build_prompt(
    question,
    results
):

    context = ""

    for item in results:
        # `item` is expected to be a dict like:
        # {"text": ..., "source": ..., "page": ..., "score": ...}
        if not isinstance(item, dict):
            # Gracefully handle unexpected result shapes
            item = {"source": str(item), "page": "", "text": str(item)}

        context += f"""

Document :
{item.get('source', '')}

Page :
{item.get('page', '')}

Content :
{item.get('text', '')}

"""


    prompt = f"""
You are an intelligent Retrieval-Augmented Generation (RAG) assistant.

Answer ONLY using the provided context.

Never invent information.

If the answer is unavailable, reply:

"I couldn't find the answer in the uploaded documents."

=========================

Context

{context}

=========================

Question

{question}

=========================

Answer
"""

    return prompt


# ----------------------------------------
# Gemini
# ----------------------------------------


def ask_gemini(
    question,
    results
):

    prompt = build_prompt(
        question,
        results
    )

    try:

        response = client.models.generate_content(

            model="gemini-2.5-flash",

            contents=prompt

        )

        return response.text

    except Exception as e:

        return f"Gemini Error:\n{e}"


# ----------------------------------------
# Save Index
# ----------------------------------------


def save_index(
    index,
    path="vectorstore/index.faiss"
):

    faiss.write_index(
        index,
        path
    )


# ----------------------------------------
# Load Index
# ----------------------------------------


def load_index(
    path="vectorstore/index.faiss"
):

    return faiss.read_index(
        path
    )