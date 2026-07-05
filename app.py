import streamlit as st

from styles import load_css

from sidebar import sidebar

from ui import (

    hero_section,

    suggestion_cards,

    chat_interface

)

from rag import (

    create_vector_store,

    search_chunks,

    ask_gemini

)
from utils import (

    process_documents,

    split_text

)
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

    st.session_state.messages=[]

if "chunks" not in st.session_state:

    st.session_state.chunks=[]

if "index" not in st.session_state:

    st.session_state.index=None

if "documents_loaded" not in st.session_state:

    st.session_state.documents_loaded=False

# ==========================================
# SIDEBAR
# ==========================================

sidebar_data = sidebar()

uploaded_files = sidebar_data["uploaded_files"]

top_k = sidebar_data["top_k"]

chunk_size = sidebar_data["chunk_size"]

overlap = sidebar_data["overlap"]

# ==========================================
# HERO
# ==========================================

hero_section()

suggestion_cards()
hero_section()

suggestion_cards()
# ==========================================
# DOCUMENT PROCESSING
# ==========================================

if uploaded_files:

    with st.spinner("📚 Reading Documents..."):

        pages = process_documents(uploaded_files)

    with st.spinner("✂ Splitting Documents..."):

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

            "🤖 AI",

            "Ready"

        )

else:

    st.info(

        "👈 Upload one or more documents from the sidebar."

    )
# ==========================================
# CHATBOT
# ==========================================

if st.session_state.documents_loaded:

    answer = chat_interface(

        chunks=st.session_state.chunks,

        index=st.session_state.index,

        top_k=top_k,

        search_function=search_chunks,

        llm_function=ask_gemini

    )

    # --------------------------------------
    # EXPORT CHAT
    # --------------------------------------

    st.markdown("---")

    st.subheader("📥 Export Conversation")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.download_button(

            "📄 Export TXT",

            export_txt(

                st.session_state.messages

            ),

            "chat.txt",

            use_container_width=True,

            key="export_txt"

        )

    with col2:

        st.download_button(

            "📝 Export Markdown",

            export_markdown(

                st.session_state.messages

            ),

            "chat.md",

            use_container_width=True,

            key="export_md"

        )

    with col3:

        pdf_file = export_pdf(

            st.session_state.messages

        )

        with open(

            pdf_file,

            "rb"

        ) as pdf:

            st.download_button(

                "📕 Export PDF",

                pdf,

                "chat.pdf",

                use_container_width=True,

                key="export_pdf"

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

Then start chatting with your documents.
"""

    )
# ==========================================
# ANALYTICS
# ==========================================

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

# ==========================================
# PROJECT INFORMATION
# ==========================================

with st.expander(
    "ℹ About",
    expanded=False
):

    st.markdown("""

## 🤖 RAG Chatbot Pro

Professional Retrieval-Augmented Generation Chatbot

### Technologies

- Streamlit

- Google Gemini

- FAISS

- Sentence Transformers

- Python

- ReportLab

- Pandas

- NumPy

### Supported Documents

- PDF

- DOCX

- TXT

- CSV

- Excel

""")

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

left, center, right = st.columns(3)

with left:

    st.caption(
        "🤖 Gemini AI"
    )

with center:

    st.caption(
        "🔍 FAISS Search"
    )

with right:

    st.caption(
        "⚡ Streamlit"
    )

st.markdown(
    """
<div align="center">

### ✨ RAG Chatbot Pro

Made with ❤️ by **Siva Prasad**

</div>
""",
    unsafe_allow_html=True
)
