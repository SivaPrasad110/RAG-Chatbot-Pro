import streamlit as st

# ================================
# UI
# ================================

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

# ================================
# RAG
# ================================

from rag import (
    create_vector_store,
    search_chunks,
    ask_gemini
)

# ================================
# DOCUMENTS
# ================================

from utils import (
    process_documents,
    split_text
)

# ================================
# EXPORT
# ================================

from export import (
    export_txt,
    export_markdown,
    export_pdf
)

# ================================
# PAGE CONFIG
# ================================

st.set_page_config(
    page_title="RAG Chatbot Pro",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================================
# LOAD CSS
# ================================

load_css()

# ================================
# SESSION STATE
# ================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chunks" not in st.session_state:
    st.session_state.chunks = []

if "index" not in st.session_state:
    st.session_state.index = None

if "documents_loaded" not in st.session_state:
    st.session_state.documents_loaded = False

# ================================
# SIDEBAR
# ================================

sidebar_data = sidebar()

uploaded_files = sidebar_data["uploaded_files"]

top_k = sidebar_data["top_k"]

chunk_size = sidebar_data["chunk_size"]

overlap = sidebar_data["overlap"]
# ==========================================
# HERO SECTION
# ==========================================

hero_section()

suggestion_cards()

st.markdown("---")

# ==========================================
# DOCUMENT PROCESSING
# ==========================================

if uploaded_files and not st.session_state.documents_loaded:

    with st.spinner("📚 Reading uploaded documents..."):

        pages = process_documents(uploaded_files)

        pages = [
            page for page in pages
            if page.get("text", "").strip()
        ]

    if len(pages) == 0:

        st.error("No readable content found in the uploaded documents.")

    else:

        with st.spinner("✂️ Splitting documents into chunks..."):

            chunks = split_text(

                pages,

                chunk_size=chunk_size,

                overlap=overlap

            )

        with st.spinner("🧠 Creating Vector Database..."):

            index = create_vector_store(chunks)

        st.session_state.chunks = chunks

        st.session_state.index = index

        st.session_state.documents_loaded = True

        st.success("✅ Documents processed successfully!")

        st.markdown("### 📊 Workspace")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(

                "📄 Documents",

                len(uploaded_files)

            )

        with col2:

            st.metric(

                "📚 Chunks",

                len(chunks)

            )

        with col3:

            st.metric(

                "🤖 AI Status",

                "Ready"

            )

else:

    welcome_screen()
# ==========================================
# CHAT INTERFACE
# ==========================================

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
📂 Upload your documents from the sidebar.

Once uploaded, you can ask questions about your documents.
"""
    )

# ==========================================
# AI STATUS
# ==========================================

st.markdown("---")

ai_status()

# ==========================================
# CHAT STATISTICS
# ==========================================

conversation_stats()
# ==========================================
# EXPORT CHAT
# ==========================================

if len(st.session_state.messages) > 0:

    st.markdown("---")

    st.subheader("📥 Export Conversation")

    col1, col2, col3 = st.columns(3)

    # TXT
    with col1:

        st.download_button(

            label="📄 TXT",

            data=export_txt(
                st.session_state.messages
            ),

            file_name="chat.txt",

            mime="text/plain",

            use_container_width=True,

            key="export_txt_btn"

        )

    # Markdown
    with col2:

        st.download_button(

            label="📝 Markdown",

            data=export_markdown(
                st.session_state.messages
            ),

            file_name="chat.md",

            mime="text/markdown",

            use_container_width=True,

            key="export_md_btn"

        )

    # PDF
    with col3:

        try:

            pdf_path = export_pdf(
                st.session_state.messages
            )

            with open(pdf_path, "rb") as pdf:

                st.download_button(

                    label="📕 PDF",

                    data=pdf,

                    file_name="chat.pdf",

                    mime="application/pdf",

                    use_container_width=True,

                    key="export_pdf_btn"

                )

        except Exception as e:

            st.warning(
                f"Unable to generate PDF: {e}"
            )

# ==========================================
# FOOTER
# ==========================================

footer()
