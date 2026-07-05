import os
import streamlit as st

from utils import (
    read_pdf,
    read_docx,
    read_txt,
    read_csv,
    read_excel,
    split_text
)

from rag import (
    create_vector_store,
    search_chunks,
    ask_gemini
)

from analytics import show_dashboard
from export import (
    export_txt,
    export_markdown,
    export_pdf
)

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Professional RAG Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================
# CUSTOM CSS (ChatGPT Style)
# =====================================

st.markdown("""
<style>

.block-container{
    padding-top:2rem;
}

h1{
    text-align:center;
}

.stChatMessage{
    border-radius:15px;
}

.stButton>button{
    width:100%;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# SESSION STATE
# =====================================

if "messages" not in st.session_state:
    st.session_state.messages=[]

if "chunks" not in st.session_state:
    st.session_state.chunks=[]

if "index" not in st.session_state:
    st.session_state.index=None

if "documents_loaded" not in st.session_state:
    st.session_state.documents_loaded=False

# =====================================
# SIDEBAR
# =====================================

with st.sidebar:

    st.title("🤖 RAG Chatbot")

    st.markdown("---")

    st.subheader("📂 Upload Documents")

    uploaded_files = st.file_uploader(
        "Upload Files",
        type=[
            "pdf",
            "docx",
            "txt",
            "csv",
            "xlsx"
        ],
        accept_multiple_files=True
    )

    st.markdown("---")

    st.subheader("⚙ Settings")

    top_k = st.slider(
        "Top Matching Chunks",
        1,
        10,
        3
    )

    chunk_size = st.slider(
        "Chunk Size",
        200,
        1200,
        600,
        100
    )

    overlap = st.slider(
        "Chunk Overlap",
        0,
        300,
        100,
        20
    )

    st.markdown("---")

    st.subheader("📥 Export Chat")

    txt_data = export_txt(
        st.session_state.messages
    )

    st.download_button(
        "Download TXT",
        txt_data,
        "chat.txt"
    )

    md_data = export_markdown(
        st.session_state.messages
    )

    st.download_button(
        "Download Markdown",
        md_data,
        "chat.md"
    )

    if st.button("Generate PDF"):

        pdf_path = export_pdf(
            st.session_state.messages
        )

        with open(pdf_path,"rb") as pdf:

            st.download_button(
                "Download PDF",
                pdf,
                "chat.pdf"
            )

    st.markdown("---")

    if st.button("🗑 Clear Chat"):

        st.session_state.messages=[]

        st.rerun()

# =====================================
# MAIN TITLE
# =====================================

st.title("🤖 Professional RAG Chatbot")

st.caption(
    "Powered by Gemini • FAISS • Sentence Transformers"
)
# =====================================
# DOCUMENT PROCESSING
# =====================================

if uploaded_files:

    all_pages = []

    with st.spinner("📚 Reading uploaded documents..."):

        progress = st.progress(0)

        total_files = len(uploaded_files)

        for i, file in enumerate(uploaded_files):

            extension = os.path.splitext(file.name)[1].lower()

            try:

                # --------------------
                # PDF
                # --------------------

                if extension == ".pdf":

                    pages = read_pdf(file)

                    for page in pages:

                        page["source"] = file.name

                    all_pages.extend(pages)

                # --------------------
                # DOCX
                # --------------------

                elif extension == ".docx":

                    pages = read_docx(file)

                    for page in pages:

                        page["source"] = file.name

                    all_pages.extend(pages)

                # --------------------
                # TXT
                # --------------------

                elif extension == ".txt":

                    pages = read_txt(file)

                    for page in pages:

                        page["source"] = file.name

                    all_pages.extend(pages)

                # --------------------
                # CSV
                # --------------------

                elif extension == ".csv":

                    pages = read_csv(file)

                    for page in pages:

                        page["source"] = file.name

                    all_pages.extend(pages)

                # --------------------
                # Excel
                # --------------------

                elif extension == ".xlsx":

                    pages = read_excel(file)

                    for page in pages:

                        page["source"] = file.name

                    all_pages.extend(pages)

            except Exception as e:

                st.error(f"❌ Error reading {file.name}")

                st.exception(e)

            progress.progress((i + 1) / total_files)

        progress.empty()

# =====================================
# DOCUMENT SUMMARY
# =====================================

    st.success(
        f"✅ Successfully loaded {len(uploaded_files)} document(s)"
    )

    with st.expander(
        "📂 Uploaded Documents",
        expanded=False
    ):

        for file in uploaded_files:

            st.write(
                f"📄 {file.name}"
            )

# =====================================
# CHUNKING
# =====================================

    with st.spinner("✂ Splitting documents into chunks..."):

        chunks = split_text(
            all_pages,
            chunk_size=chunk_size,
            overlap=overlap
        )

# =====================================
# VECTOR STORE
# =====================================

    with st.spinner("🧠 Creating Vector Database..."):

        index = create_vector_store(
            chunks
        )

# =====================================
# SAVE SESSION
# =====================================

    st.session_state.chunks = chunks

    st.session_state.index = index

    st.session_state.documents_loaded = True

    st.sidebar.markdown("---")

    st.sidebar.success(
        f"📚 Total Chunks : {len(chunks)}"
    )

# =====================================
# CHAT HISTORY
# =====================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )
# =====================================
# CHAT INPUT
# =====================================

if st.session_state.documents_loaded:

    question = st.chat_input(
        "💬 Ask anything about your uploaded documents..."
    )

    if question:

        # ----------------------------------
        # Save User Message
        # ----------------------------------

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):
            st.markdown(question)

        # ----------------------------------
        # Search Similar Chunks
        # ----------------------------------

        with st.spinner("🔍 Searching documents..."):

            results = search_chunks(
                question=question,
                chunks=st.session_state.chunks,
                index=st.session_state.index,
                top_k=top_k
            )

        # ----------------------------------
        # Build Context
        # (Hidden from User)
        # ----------------------------------

        context = ""

        for item in results:

            context += f"""

Document : {item['source']}

Page : {item['page']}

Content :

{item['text']}

"""

        # ----------------------------------
        # Gemini
        # ----------------------------------

        with st.spinner("🤖 Gemini is thinking..."):

            answer = ask_gemini(
                question,
                context
            )

        # ----------------------------------
        # Save Assistant Message
        # ----------------------------------

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        # ----------------------------------
        # Display Assistant
        # ----------------------------------

        with st.chat_message("assistant"):

            st.markdown(answer)

        # ----------------------------------
        # Analytics
        # ----------------------------------

        try:

            show_dashboard(
                st.session_state.messages
            )

        except:
            pass

        # ----------------------------------
        # Export Buttons
        # ----------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:

            st.download_button(
                "📄 TXT",
                export_txt(
                    st.session_state.messages
                ),
                "chat.txt",
                mime="text/plain"
            )

        with col2:

            st.download_button(
                "📝 Markdown",
                export_markdown(
                    st.session_state.messages
                ),
                "chat.md",
                mime="text/markdown"
            )

        with col3:

            pdf_path = export_pdf(
                st.session_state.messages
            )

            with open(pdf_path, "rb") as pdf:

                st.download_button(
                    "📕 PDF",
                    pdf,
                    "chat.pdf"
                )

# =====================================
# NO DOCUMENTS
# =====================================

else:

    st.info(
        """
👈 Upload one or more documents from the sidebar.

Supported formats:

• PDF
• DOCX
• TXT
• CSV
• Excel
"""
    )
# =====================================
# ANALYTICS DASHBOARD
# =====================================

st.markdown("---")

with st.expander("📊 Chat Analytics", expanded=False):

    total_messages = len(st.session_state.messages)

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

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "💬 Total Messages",
        total_messages
    )

    col2.metric(
        "👤 User",
        user_messages
    )

    col3.metric(
        "🤖 Assistant",
        assistant_messages
    )

    if st.button("📈 Open Dashboard"):

        try:

            show_dashboard(
                st.session_state.messages
            )

        except Exception:

            st.info("Analytics Dashboard not available.")

# =====================================
# ABOUT
# =====================================

with st.expander("ℹ About This Project", expanded=False):

    st.markdown("""
### Professional RAG Chatbot

This chatbot supports:

✅ PDF

✅ DOCX

✅ TXT

✅ CSV

✅ Excel

✅ FAISS Vector Search

✅ Sentence Transformers

✅ Gemini AI

✅ Conversation Memory

✅ Export Chat

✅ Analytics Dashboard

Built using:

- Streamlit
- Google Gemini
- FAISS
- Sentence Transformers
- Python
""")

# =====================================
# FOOTER
# =====================================

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:

    st.caption("🤖 Gemini AI")

with col2:

    st.caption("🔍 FAISS Vector Search")

with col3:

    st.caption("⚡ Streamlit")

st.markdown(
    "<center><h5>🚀 Professional RAG Chatbot</h5></center>",
    unsafe_allow_html=True
)

st.caption(
    "Made with ❤️ using Python, Streamlit, Gemini AI and FAISS."
)
