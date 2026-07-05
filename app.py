import streamlit as st
import os


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
from export import export_txt, export_markdown, export_pdf

# ===================================
# PAGE CONFIG
# ===================================

st.set_page_config(

    page_title="Professional RAG Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===================================
# SESSION STATE
# ===================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chunks" not in st.session_state:
    st.session_state.chunks = []

if "index" not in st.session_state:
    st.session_state.index = None

if "documents_loaded" not in st.session_state:
    st.session_state.documents_loaded = False

if "theme" not in st.session_state:
    st.session_state.theme = "Light"

# ===================================
# SIDEBAR
# ===================================

with st.sidebar:

    st.title("🤖 RAG Chatbot")

    # Sidebar controls (upload/scalars/voice)


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
        min_value=1,
        max_value=10,
        value=3
    )

    chunk_size = st.slider(
        "Chunk Size",
        200,
        1000,
        500,
        step=100
    )

    overlap = st.slider(
        "Chunk Overlap",
        0,
        300,
        100,
        step=20
    )

    from speech import (
        speak,
        listen
    )

    st.markdown("---")

    st.subheader("🎤 Voice")

    voice_question = ""

    if st.button("🎙 Speak Question"):
        voice_question = listen()
        if voice_question:
            st.success(voice_question)

    st.caption("(Use the chat input below to send questions.)")

    # Optional: speak last assistant answer
    if st.button("🔊 Read Last Answer"):
        if st.session_state.messages:
            last_msg = st.session_state.messages[-1]
            if last_msg.get("role") == "assistant":
                speak(last_msg.get("content", ""))

    st.sidebar.subheader("📥 Export Chat")

    txt_data = export_txt(
        st.session_state.messages
    )

    st.sidebar.download_button(
        "TXT",
        txt_data,
        "chat.txt"
    )

    md_data = export_markdown(
        st.session_state.messages
    )

    st.sidebar.download_button(
        "Markdown",
        md_data,
        "chat.md"
    )

if st.sidebar.button("Generate PDF"):

    pdf_path = export_pdf(
        st.session_state.messages
    )

    with open(pdf_path, "rb") as pdf:

        st.sidebar.download_button(
            "Download PDF",
            pdf,
            "chat.pdf"
        )
    st.markdown("---")

    st.subheader("🎨 Theme")

    st.session_state.theme = st.selectbox(
        "Select Theme",
        [
            "Light",
            "Dark"
        ]
    )

    st.markdown("---")

    if st.button("🗑 Clear Chat"):

        st.session_state.messages = []

        st.rerun()

# ===================================
# TITLE
# ===================================

st.title("🤖 Professional RAG Chatbot")

st.caption(
    "Upload your documents and ask intelligent questions using Gemini AI + FAISS."
)

# ===================================
# DOCUMENT PROCESSING
# ===================================

if uploaded_files:

    all_pages = []

    with st.spinner("📚 Reading documents..."):

        progress = st.progress(0)

        total_files = len(uploaded_files)

        for i, file in enumerate(uploaded_files):

            try:

                extension = os.path.splitext(file.name)[1].lower()

                if extension == ".pdf":
                    all_pages.extend(read_pdf(file))

                elif extension == ".docx":
                    all_pages.extend(read_docx(file))

                elif extension == ".txt":
                    all_pages.extend(read_txt(file))

                elif extension == ".csv":
                    all_pages.extend(read_csv(file))

                elif extension == ".xlsx":
                    all_pages.extend(read_excel(file))

            except Exception as e:

                st.error(f"Error reading {file.name}")

                st.exception(e)

            progress.progress((i + 1) / total_files)

        progress.empty()

    st.success(f"Loaded {len(uploaded_files)} documents")

    st.sidebar.markdown("---")
    st.sidebar.subheader("📄 Uploaded Files")

    for file in uploaded_files:
        st.sidebar.success(file.name)

    chunks = split_text(
        all_pages,
        chunk_size=chunk_size,
        overlap=overlap
    )

    with st.spinner("🔍 Creating Vector Database..."):

        index = create_vector_store(chunks)

    st.session_state.chunks = chunks
    st.session_state.index = index
    st.session_state.documents_loaded = True

# ===================================
# CHAT HISTORY
# ===================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# ===================================
# CHAT INPUT
# ===================================

if st.session_state.documents_loaded:

    question = st.chat_input(
        "Ask anything about your uploaded documents..."
    )

    if question:

        # -------------------------
        # USER MESSAGE
        # -------------------------

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):
            st.markdown(question)

        # -------------------------
        # SEARCH
        # -------------------------

        with st.spinner("Searching..."):

            results = search_chunks(
                question,
                st.session_state.chunks,
                st.session_state.index,
                top_k
            )

        # -------------------------
        # CREATE CONTEXT
        # -------------------------

        context = ""

        for item in results:

            context += f"""

Document : {item['source']}

Page : {item['page']}

Content :

{item['text']}

"""

        # -------------------------
        # GEMINI
        # -------------------------

        with st.spinner("Gemini is thinking..."):

            answer = ask_gemini(
                question,
                context
            )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        # -------------------------
        # ASSISTANT
        # -------------------------

        with st.chat_message("assistant"):

            st.markdown(answer)

            st.markdown("---")

            st.subheader("📚 Sources")

            for i, item in enumerate(results):

                st.markdown(
                    f"""
### 📄 {item['source']}

**Page:** {item['page']}
"""
                )

                # Similarity Score
                if "score" in item:
                    try:
                        raw = float(item["score"])
                        # FAISS inner-product can exceed 1; clamp to valid Streamlit range.
                        clamped = max(0.0, min(raw, 1.0))
                    except Exception:
                        clamped = 0.0

                    st.progress(clamped)

                    st.caption(
                        f"Similarity : {item['score']:.2f}"
                    )

                st.info(item["text"])

        # -------------------------
        # EXPORT
        # -------------------------

        st.download_button(
            label="📥 Export Chat",
            data=answer,
            file_name="chat.txt",
            mime="text/plain"
        )

        # -------------------------
        # TEXT TO SPEECH
        # -------------------------

        tts_html = f"""
        <script>
        let speech = new SpeechSynthesisUtterance();
        speech.text = `{answer}`;
        speech.lang = 'en-US';
        speech.rate = 1;
        speech.pitch = 1;
        </script>
        """

        st.components.v1.html(
            tts_html,
            height=0
        )

else:

    st.info(
        "👈 Upload one or more documents from the sidebar."
    )

# ===================================
# FOOTER
# ===================================

st.markdown("---")

st.caption(
    "Professional RAG Chatbot | Gemini • FAISS • Sentence Transformers • Streamlit"
)