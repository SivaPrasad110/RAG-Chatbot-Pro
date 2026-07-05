import streamlit as st

# ==========================================
# UI
# ==========================================

from styles import load_css
from sidebar import sidebar

from ui import (
    hero_section,
    suggestion_cards,
    welcome_screen,
    chat_interface,
    conversation_stats,
    ai_status,
    footer
)

# ==========================================
# RAG
# ==========================================

from rag import (
    create_vector_store,
    search_chunks,
    ask_gemini      # (This now uses Groq internally)
)

# ==========================================
# DOCUMENTS
# ==========================================

from utils import (
    process_documents,
    split_text
)

# ==========================================
# EXPORT
# ==========================================

from export import (
    export_txt,
    export_markdown,
    export_pdf
)

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(

    page_title="RAG Chatbot Pro",

    page_icon="🤖",

    layout="wide",

    initial_sidebar_state="expanded"

)

# ==========================================
# LOAD CSS
# ==========================================

load_css()

# ==========================================
# SESSION STATE
# ==========================================

if "messages" not in st.session_state:

    st.session_state.messages = []

if "chunks" not in st.session_state:

    st.session_state.chunks = []

if "index" not in st.session_state:

    st.session_state.index = None

if "documents_loaded" not in st.session_state:

    st.session_state.documents_loaded = False

# ==========================================
# SIDEBAR
# ==========================================

sidebar_data = sidebar()

uploaded_files = sidebar_data["uploaded_files"]

top_k = sidebar_data["top_k"]

chunk_size = sidebar_data["chunk_size"]

overlap = sidebar_data["overlap"]
# =====================================================
# HERO SECTION
# =====================================================

hero_section()

suggestion_cards()

st.markdown("---")


# =====================================================
# DOCUMENT PROCESSING
# =====================================================

if uploaded_files and not st.session_state.documents_loaded:

    with st.spinner("📚 Reading uploaded documents..."):

        pages = process_documents(uploaded_files)

    # Remove empty pages
    pages = [

        page

        for page in pages

        if page.get("text", "").strip()

    ]

    if len(pages) == 0:

        st.error(
            "❌ No readable text found in the uploaded documents."
        )

    else:

        # ------------------------------------
        # Split Documents
        # ------------------------------------

        with st.spinner("✂ Splitting documents..."):

            chunks = split_text(

                pages,

                chunk_size=chunk_size,

                overlap=overlap

            )

        # ------------------------------------
        # Create Vector Store
        # ------------------------------------

        with st.spinner("🧠 Creating Vector Database..."):

            index = create_vector_store(

                chunks

            )

        # ------------------------------------
        # Save to Session
        # ------------------------------------

        st.session_state.chunks = chunks

        st.session_state.index = index

        st.session_state.documents_loaded = True

        st.success(
            "✅ Documents processed successfully!"
        )

        # ------------------------------------
        # Workspace Dashboard
        # ------------------------------------

        st.markdown("## 📊 Workspace")

        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(

                "📄 Documents",

                len(uploaded_files)

            )

        with c2:

            st.metric(

                "📚 Chunks",

                len(chunks)

            )

        with c3:

            st.metric(

                "🤖 AI",

                "Groq Ready"

            )

# =====================================================
# NO DOCUMENTS
# =====================================================

elif not st.session_state.documents_loaded:

    welcome_screen()
# =====================================================
# CHAT INTERFACE
# =====================================================

if st.session_state.documents_loaded:

    answer = chat_interface(

        chunks=st.session_state.chunks,

        index=st.session_state.index,

        top_k=top_k,

        search_function=search_chunks,

        llm_function=ask_gemini

    )

else:

    st.info(
        """
👋 Welcome!

Upload one or more documents from the sidebar.

Supported formats

• PDF

• DOCX

• TXT

• CSV

• Excel

After uploading, start asking questions about your documents.
"""
    )

# =====================================================
# AI STATUS
# =====================================================

st.markdown("---")

ai_status()

# =====================================================
# CONVERSATION STATISTICS
# =====================================================

conversation_stats()
# =====================================================
# EXPORT CONVERSATION
# =====================================================

if len(st.session_state.messages) > 0:

    st.markdown("---")

    st.subheader("📥 Export Conversation")

    col1, col2, col3 = st.columns(3)

    # TXT
    with col1:

        st.download_button(

            label="📄 Export TXT",

            data=export_txt(
                st.session_state.messages
            ),

            file_name="chat.txt",

            mime="text/plain",

            use_container_width=True,

            key="export_txt"

        )

    # Markdown
    with col2:

        st.download_button(

            label="📝 Export Markdown",

            data=export_markdown(
                st.session_state.messages
            ),

            file_name="chat.md",

            mime="text/markdown",

            use_container_width=True,

            key="export_md"

        )

    # PDF
    with col3:

        try:

            pdf_path = export_pdf(
                st.session_state.messages
            )

            with open(pdf_path, "rb") as pdf:

                st.download_button(

                    label="📕 Export PDF",

                    data=pdf,

                    file_name="chat.pdf",

                    mime="application/pdf",

                    use_container_width=True,

                    key="export_pdf"

                )

        except Exception as e:

            st.warning(
                f"Unable to generate PDF: {e}"
            )

# =====================================================
# ANALYTICS
# =====================================================

st.markdown("---")

with st.expander(
    "📊 Analytics",
    expanded=False
):

    total_messages = len(
        st.session_state.messages
    )

    user_messages = len(
        [
            msg
            for msg in st.session_state.messages
            if msg["role"] == "user"
        ]
    )

    assistant_messages = len(
        [
            msg
            for msg in st.session_state.messages
            if msg["role"] == "assistant"
        ]
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "💬 Total",
            total_messages
        )

    with c2:
        st.metric(
            "👤 User",
            user_messages
        )

    with c3:
        st.metric(
            "🤖 AI",
            assistant_messages
        )

# =====================================================
# ABOUT
# =====================================================

with st.expander(
    "ℹ️ About",
    expanded=False
):

    st.markdown("""

## 🤖 RAG Chatbot Pro

An AI-powered document assistant built with Retrieval-Augmented Generation (RAG).

### 🚀 Features

- 📄 PDF, DOCX, TXT, CSV & Excel Support
- 🔍 Semantic Search using FAISS
- 🧠 Sentence Transformers
- 🤖 Groq Llama 3.3 Integration
- 💬 Conversational AI
- 📥 Export Chat
- 📊 Analytics Dashboard
- 🌐 Streamlit Deployment

### 🛠 Tech Stack

- Python
- Streamlit
- FAISS
- Sentence Transformers
- Groq API
- OpenAI SDK
- Pandas
- NumPy
- ReportLab

""")

# =====================================================
# FOOTER
# =====================================================

footer()
