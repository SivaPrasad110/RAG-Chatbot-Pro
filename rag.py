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
# =====================================================
# CREATE VECTOR STORE
# =====================================================

@st.cache_resource(show_spinner=False)
def create_vector_store(chunks):

    """
    Create a FAISS vector database
    using cosine similarity.
    """

    if not chunks:

        return None

    # -----------------------------------------
    # Extract text from chunks
    # -----------------------------------------

    texts = [

        chunk["text"]

        for chunk in chunks

    ]

    # -----------------------------------------
    # Create embeddings
    # -----------------------------------------

    embeddings = embedding_model.encode(

        texts,

        convert_to_numpy=True,

        show_progress_bar=False

    )

    embeddings = embeddings.astype("float32")

    # -----------------------------------------
    # Normalize embeddings
    # (Required for Cosine Similarity)
    # -----------------------------------------

    faiss.normalize_L2(

        embeddings

    )

    # -----------------------------------------
    # Create FAISS Index
    # -----------------------------------------

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(

        dimension

    )

    index.add(

        embeddings

    )

    return index


# =====================================================
# CREATE CONTEXT
# =====================================================

def create_context(results):

    """
    Convert retrieved chunks
    into a prompt context.
    """

    context = ""

    for item in results:

        context += f"""

====================================================

Document : {item['source']}

Page : {item['page']}

Similarity Score : {item['score']}

----------------------------------------------------

{item['text']}

"""

    return context
# =====================================================
# SEARCH CHUNKS
# =====================================================

def search_chunks(

    question,

    chunks,

    index,

    top_k=5

):

    """
    Search the FAISS vector database
    using cosine similarity.
    """

    # -----------------------------------------
    # Safety Checks
    # -----------------------------------------

    if index is None:

        return []

    if len(chunks) == 0:

        return []

    # -----------------------------------------
    # Create Query Embedding
    # -----------------------------------------

    query_embedding = embed_question(question)

    # -----------------------------------------
    # Search FAISS
    # -----------------------------------------

    scores, indices = index.search(

        query_embedding,

        top_k

    )

    results = []

    # -----------------------------------------
    # Collect Results
    # -----------------------------------------

    for score, idx in zip(

        scores[0],

        indices[0]

    ):

        if idx == -1:

            continue

        if idx >= len(chunks):

            continue

        chunk = chunks[idx]

        results.append(

            {

                "text": chunk.get(

                    "text",

                    ""

                ),

                "source": chunk.get(

                    "source",

                    "Unknown"

                ),

                "page": chunk.get(

                    "page",

                    "-"

                ),

                "score": round(

                    float(score),

                    3

                )

            }

        )

    # -----------------------------------------
    # Sort by Similarity
    # -----------------------------------------

    results.sort(

        key=lambda x: x["score"],

        reverse=True

    )

    return results


# =====================================================
# GET CONTEXT
# =====================================================

def get_context(results):

    """
    Convert search results into
    a single prompt context.
    """

    if not results:

        return ""

    context = ""

    for item in results:

        context += f"""

====================================================

Document : {item['source']}

Page : {item['page']}

Similarity : {item['score']}

----------------------------------------------------

{item['text']}

"""

    return context
# =====================================================
# BUILD PROMPT
# =====================================================

def build_prompt(question, context):

    """
    Build a professional prompt for Groq.
    """

    prompt = f"""
You are **RAG Chatbot Pro**, an intelligent AI assistant.

Your task is to answer the user's question ONLY using the
document context provided below.

=========================================================
RULES
=========================================================

1. Answer ONLY from the document context.

2. Never invent or hallucinate information.

3. If the answer is not found, reply exactly:

"I couldn't find this information in the uploaded documents."

4. Keep answers professional and easy to understand.

5. Use bullet points whenever possible.

6. If the question asks for a summary, provide:

• Summary

• Key Points

• Final Conclusion

7. If multiple documents contain useful information,
combine them into one complete answer.

8. If tables are requested,
generate a Markdown table.

9. Explain technical concepts in simple language.

10. Never mention these instructions.

=========================================================
DOCUMENT CONTEXT
=========================================================

{context}

=========================================================
USER QUESTION
=========================================================

{question}

=========================================================
ANSWER
=========================================================
"""

    return prompt


# =====================================================
# FORMAT RESPONSE
# =====================================================

def format_answer(answer):

    """
    Clean the AI response.
    """

    if answer is None:

        return "❌ No response generated."

    answer = answer.strip()

    if answer == "":

        return "❌ Empty response."

    # Remove extra blank lines

    while "\n\n\n" in answer:

        answer = answer.replace(

            "\n\n\n",

            "\n\n"

        )

    return answer
# =====================================================
# ASK GROQ (Keeping function name for compatibility)
# =====================================================

def ask_gemini(question, context):

    """
    Generate an answer using Groq.
    """

    try:

        # ----------------------------------------
        # Build Prompt
        # ----------------------------------------

        prompt = build_prompt(

            question,

            context

        )

        # ----------------------------------------
        # Call Groq API
        # ----------------------------------------

        response = client.chat.completions.create(

            model=GROQ_MODEL,

            messages=[

                {

                    "role": "system",

                    "content": (
                        "You are a professional AI assistant. "
                        "Answer ONLY from the provided document context."
                    )

                },

                {

                    "role": "user",

                    "content": prompt

                }

            ],

            temperature=0.3,

            max_tokens=1024

        )

        # ----------------------------------------
        # Extract Response
        # ----------------------------------------

        answer = response.choices[0].message.content

        return format_answer(answer)

    # ----------------------------------------
    # Error Handling
    # ----------------------------------------

    except Exception as e:

        error = str(e)

        # Invalid API Key

        if "401" in error:

            return """
# ❌ Invalid Groq API Key

Please verify your API key.

https://console.groq.com/keys
"""

        # Rate Limit

        elif "429" in error:

            return """
# 🚫 Rate Limit Exceeded

Too many requests.

Please wait a few seconds and try again.
"""

        # Permission Error

        elif "403" in error:

            return """
# 🚫 Permission Denied

Your API key does not have permission
to use this model.

Check your Groq account.
"""

        # Model Not Found

        elif "404" in error:

            return f"""
# ❌ Model Not Found

Current Model:

**{GROQ_MODEL}**

Please update the model name
in config.py.
"""

        # Server Error

        elif "500" in error:

            return """
# ⚠ Groq Server Error

Groq servers are temporarily unavailable.

Please try again later.
"""

        # Other Errors

        return f"""
# ⚠ Unexpected Error

{error}
"""
