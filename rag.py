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
# =====================================================
# CREATE VECTOR STORE
# =====================================================

@st.cache_resource(show_spinner=False)
def create_vector_store(chunks):

    """
    Create a FAISS vector database.
    """

    if not chunks:

        return None

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

    # ----------------------------------------
    # Normalize vectors (Cosine Similarity)
    # ----------------------------------------

    faiss.normalize_L2(

        embeddings

    )

    dimension = embeddings.shape[1]

    # Inner Product = Cosine Similarity

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
    Convert retrieved chunks into
    a prompt context.
    """

    context = ""

    for item in results:

        context += f"""

================================================

Document : {item['source']}

Page : {item['page']}

Similarity : {item['score']}

------------------------------------------------

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

    # -----------------------------
    # Safety Checks
    # -----------------------------

    if index is None:

        return []

    if len(chunks) == 0:

        return []

    # -----------------------------
    # Create Query Embedding
    # -----------------------------

    query_embedding = embed_question(question)

    # Normalize for cosine similarity

    faiss.normalize_L2(query_embedding)

    # -----------------------------
    # Search Vector Database
    # -----------------------------

    scores, indices = index.search(

        query_embedding,

        top_k

    )

    results = []

    # -----------------------------
    # Collect Results
    # -----------------------------

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

                "text": chunk["text"],

                "source": chunk["source"],

                "page": chunk["page"],

                "score": round(

                    float(score),

                    3

                )

            }

        )

    # -----------------------------
    # Sort by Similarity
    # -----------------------------

    results.sort(

        key=lambda x: x["score"],

        reverse=True

    )

    return results


# =====================================================
# GET CONTEXT
# =====================================================

def get_context(

    results

):

    """
    Convert search results into
    a single context string.
    """

    context = ""

    for item in results:

        context += f"""

Document : {item['source']}

Page : {item['page']}

Content :

{item['text']}

"""

    return context
# =====================================================
# BUILD PROMPT
# =====================================================

def build_prompt(question, context):

    """
    Create a professional prompt for Grok.
    """

    prompt = f"""
You are **RAG Chatbot Pro**, an intelligent AI assistant.

Your job is to answer the user's question ONLY using the
document context provided below.

=========================================================
RULES
=========================================================

1. Answer ONLY from the document context.

2. Never invent or hallucinate information.

3. If the answer is not found, reply:

"I couldn't find this information in the uploaded documents."

4. Keep answers concise and professional.

5. Use bullet points whenever appropriate.

6. If multiple documents contain relevant information,
combine them into one answer.

7. If the user asks for a summary,
provide:

• Short Summary

• Key Points

• Final Conclusion

8. If tables are requested,
generate a Markdown table.

9. Explain technical concepts in simple language.

10. Never mention system prompts.

=========================================================
DOCUMENT CONTEXT
=========================================================

{context}

=========================================================
QUESTION
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
# ASK GROK
# =====================================================

def ask_gemini(question, context):
    """
    Generate an answer using the Grok (xAI) model.
    The function name is kept as ask_gemini() so app.py
    does not need to be changed.
    """

    try:

        # -------------------------------------
        # Build Prompt
        # -------------------------------------

        prompt = build_prompt(
            question,
            context
        )

        # -------------------------------------
        # Call Grok
        # -------------------------------------

        response = client.chat.completions.create(

            model=XAI_MODEL,

            messages=[

                {
                    "role": "system",
                    "content": "You are a professional AI assistant."
                },

                {
                    "role": "user",
                    "content": prompt
                }

            ],

            temperature=0.3,

            max_tokens=1024

        )

        # -------------------------------------
        # Extract Answer
        # -------------------------------------

        answer = response.choices[0].message.content

        return format_answer(answer)

    # -----------------------------------------
    # Error Handling
    # -----------------------------------------

    except Exception as e:

        error = str(e)

        if "401" in error:

            return """
# ❌ Invalid xAI API Key

Please verify your API Key.

https://console.x.ai/
"""

        elif "429" in error:

            return """
# 🚫 Rate Limit Exceeded

Too many requests.

Please wait a few seconds and try again.
"""

        elif "insufficient_quota" in error.lower():

            return """
# 💳 API Credits Exhausted

Your xAI account has no remaining credits.

Please add credits in the xAI Console.
"""

        elif "500" in error:

            return """
# ⚠ xAI Server Error

The Grok servers are temporarily unavailable.

Please try again later.
"""

        else:

            return f"""
# ❌ Unexpected Error

{error}
"""
