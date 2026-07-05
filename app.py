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

# ===================================================
# PAGE CONFIG
# ===================================================

st.set_page_config(
    page_title="RAG Chatbot Pro",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===================================================
# CUSTOM CSS
# ===================================================

st.markdown("""
<style>

/* ----------------------------
Main Container
-----------------------------*/

.block-container{

    max-width:1150px;

    padding-top:1rem;

    padding-bottom:2rem;

}

/* ----------------------------
Sidebar
-----------------------------*/

section[data-testid="stSidebar"]{

    background:#1d1f23;

}

/* ----------------------------
Header
-----------------------------*/

.main-title{

    text-align:center;

    font-size:48px;

    font-weight:700;

    margin-bottom:5px;

}

.sub-title{

    text-align:center;

    color:gray;

    font-size:18px;

    margin-bottom:30px;

}

/* ----------------------------
Cards
-----------------------------*/

.metric-card{

    background:#262730;

    padding:15px;

    border-radius:15px;

    text-align:center;

    border:1px solid rgba(255,255,255,.05);

}

/* ----------------------------
Chat Messages
-----------------------------*/

.stChatMessage{

    border-radius:18px;

    padding:16px;

    margin-top:10px;

    margin-bottom:10px;

}

/* ----------------------------
Buttons
-----------------------------*/

.stButton>button{

    width:100%;

    border-radius:10px;

    height:45px;

}

/* ----------------------------
Download Buttons
-----------------------------*/

.stDownloadButton>button{

    width:100%;

    border-radius:10px;

}

/* ----------------------------
File Upload
-----------------------------*/

[data-testid="stFileUploader"]{

    border-radius:15px;

}

/* ----------------------------
Progress
-----------------------------*/

.stProgress{

    border-radius:20px;

}

/* ----------------------------
Hide Footer
-----------------------------*/

footer{

visibility:hidden;

}

</style>
""", unsafe_allow_html=True)

# ===================================================
# SESSION STATE
# ===================================================

if "messages" not in st.session_state:
    st.session_state.messages=[]

if "chunks" not in st.session_state:
    st.session_state.chunks=[]

if "index" not in st.session_state:
    st.session_state.index=None

if "documents_loaded" not in st.session_state:
    st.session_state.documents_loaded=False

# ===================================================
# SIDEBAR
# ===================================================

with st.sidebar:

    st.image(
        "https://streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.png",
        width=80
    )

    st.title("RAG Chatbot Pro")

    st.caption("Professional AI Document Assistant")

    st.markdown("---")

    uploaded_files=st.file_uploader(

        "📂 Upload Documents",

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

    st.subheader("⚙ AI Settings")

    top_k=st.slider(
        "Retrieved Chunks",
        1,
        10,
        3
    )

    chunk_size=st.slider(
        "Chunk Size",
        200,
        1200,
        600,
        100
    )

    overlap=st.slider(
        "Overlap",
        0,
        300,
        100,
        20
    )

    st.markdown("---")

    if st.button("🗑 Clear Chat"):

        st.session_state.messages=[]

        st.rerun()

# ===================================================
# HERO SECTION
# ===================================================

st.markdown("""
<div style="
background:linear-gradient(135deg,#4F46E5,#06B6D4);
padding:35px;
border-radius:20px;
text-align:center;
color:white;
margin-bottom:25px;
box-shadow:0px 6px 20px rgba(0,0,0,0.25);
">

<h1 style="
margin:0;
font-size:48px;
font-weight:700;
">

🤖 RAG Chatbot Pro

</h1>

<p style="
font-size:20px;
margin-top:12px;
margin-bottom:0;
">

💬 Chat with your Documents using
<b>Gemini AI + FAISS + Sentence Transformers</b>

</p>

</div>
""", unsafe_allow_html=True)

# ===================================================
# DASHBOARD
# ===================================================

c1,c2,c3,c4=st.columns(4)

with c1:

    st.metric(
        "📄 Documents",
        len(uploaded_files) if uploaded_files else 0
    )

with c2:

    st.metric(
        "🧠 Chunks",
        len(st.session_state.chunks)
    )

with c3:

    st.metric(
        "💬 Messages",
        len(st.session_state.messages)
    )

with c4:

    st.metric(
        "🤖 Model",
        "Gemini"
    )

st.markdown("---")
# ===================================================
# DOCUMENT PROCESSING
# ===================================================

if uploaded_files:

    all_pages = []

    st.success(
        f"📂 {len(uploaded_files)} document(s) selected."
    )

    with st.container(border=True):

        st.subheader("📄 Uploaded Documents")

        cols = st.columns(2)

        for i, file in enumerate(uploaded_files):

            with cols[i % 2]:

                st.success(f"✅ {file.name}")

    st.markdown("---")

    with st.spinner("📚 Reading documents..."):

        progress = st.progress(0)

        total_files = len(uploaded_files)

        status = st.empty()

        for i, file in enumerate(uploaded_files):

            extension = os.path.splitext(file.name)[1].lower()

            status.info(f"Processing : {file.name}")

            try:

                # PDF

                if extension == ".pdf":

                    pages = read_pdf(file)

                    for page in pages:
                        page["source"] = file.name

                    all_pages.extend(pages)

                # DOCX

                elif extension == ".docx":

                    pages = read_docx(file)

                    for page in pages:
                        page["source"] = file.name

                    all_pages.extend(pages)

                # TXT

                elif extension == ".txt":

                    pages = read_txt(file)

                    for page in pages:
                        page["source"] = file.name

                    all_pages.extend(pages)

                # CSV

                elif extension == ".csv":

                    pages = read_csv(file)

                    for page in pages:
                        page["source"] = file.name

                    all_pages.extend(pages)

                # Excel

                elif extension == ".xlsx":

                    pages = read_excel(file)

                    for page in pages:
                        page["source"] = file.name

                    all_pages.extend(pages)

            except Exception as e:

                st.error(f"❌ {file.name}")

                st.exception(e)

            progress.progress((i + 1) / total_files)

        progress.empty()

        status.empty()

    st.toast("🎉 Documents loaded successfully!")

    # ==========================================
    # Chunking
    # ==========================================

    with st.spinner("✂ Creating document chunks..."):

        chunks = split_text(

            all_pages,

            chunk_size=chunk_size,

            overlap=overlap

        )

    # ==========================================
    # Vector Store
    # ==========================================

    with st.spinner("🧠 Building Vector Database..."):

        index = create_vector_store(chunks)

    # Save

    st.session_state.chunks = chunks

    st.session_state.index = index

    st.session_state.documents_loaded = True

    # ==========================================
    # Statistics
    # ==========================================

    st.markdown("---")

    a, b, c = st.columns(3)

    with a:

        st.metric(

            "📄 Documents",

            len(uploaded_files)

        )

    with b:

        st.metric(

            "📚 Chunks",

            len(chunks)

        )

    with c:

        st.metric(

            "🤖 Status",

            "Ready"

        )

    st.success("✅ AI is ready. Ask your question below.")
    # ===================================================
# CHAT AREA
# ===================================================

st.markdown("## 💬 Chat")

chat_container = st.container()

with chat_container:

    # -------------------------
    # Previous Messages
    # -------------------------

    for message in st.session_state.messages:

        avatar = "👤" if message["role"] == "user" else "🤖"

        with st.chat_message(
            message["role"],
            avatar=avatar
        ):

            st.markdown(message["content"])

# ===================================================
# CHAT INPUT
# ===================================================

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

        with st.chat_message(
            "user",
            avatar="👤"
        ):

            st.markdown(question)

        # -------------------------
        # SEARCH
        # -------------------------

        with st.spinner("🔍 Searching documents..."):

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

        with st.chat_message(
            "assistant",
            avatar="🤖"
        ):

            placeholder = st.empty()

            placeholder.info(
                "🤖 Gemini is thinking..."
            )

            answer = ask_gemini(
                question,
                context
            )

            placeholder.empty()

            st.markdown(answer)

        # -------------------------
        # SAVE MESSAGE
        # -------------------------

        st.session_state.messages.append(
            {
                "role":"assistant",
                "content":answer
            }
        )

        # -------------------------
        # EXPORT
        # -------------------------

        st.markdown("---")

        col1,col2,col3=st.columns(3)

        with col1:

            st.download_button(

                "📄 TXT",

                export_txt(
                    st.session_state.messages
                ),

                "chat.txt"

            )

        with col2:

            st.download_button(

                "📝 Markdown",

                export_markdown(
                    st.session_state.messages
                ),

                "chat.md"

            )

        with col3:

            pdf_path = export_pdf(
                st.session_state.messages
            )

            with open(pdf_path,"rb") as pdf:

                st.download_button(

                    "📕 PDF",

                    pdf,

                    "chat.pdf"

                )

else:

    st.info(
        """
👋 Welcome!

Upload one or more documents from the sidebar.

Supported Files

✅ PDF

✅ DOCX

✅ TXT

✅ CSV

✅ Excel

Then start chatting with your documents.
"""
    )
# ===================================================
# SIDEBAR DASHBOARD
# ===================================================

with st.sidebar:

    st.markdown("---")

    st.subheader("📊 Dashboard")

    st.metric(
        "💬 Total Messages",
        len(st.session_state.messages)
    )

    st.metric(
        "📄 Documents",
        len(uploaded_files) if uploaded_files else 0
    )

    st.metric(
        "🧠 Chunks",
        len(st.session_state.chunks)
    )

    if st.session_state.documents_loaded:

        st.success("🟢 AI Ready")

    else:

        st.warning("🟡 Waiting for Documents")

# ===================================================
# WELCOME PAGE
# ===================================================

if not uploaded_files:

    st.markdown("<br>", unsafe_allow_html=True)

    c1,c2,c3=st.columns(3)

    with c2:

        st.image(
            "https://cdn-icons-png.flaticon.com/512/4712/4712109.png",
            width=180
        )

    st.markdown(
        """
        <h2 style='text-align:center'>
        Welcome to RAG Chatbot Pro
        </h2>

        <p style='text-align:center;color:gray;'>

        Upload your documents and start chatting with AI.

        </p>
        """,
        unsafe_allow_html=True
    )

# ===================================================
# FEATURES
# ===================================================

st.markdown("---")

st.subheader("✨ Features")

col1,col2,col3=st.columns(3)

with col1:

    st.info("""
📄 PDF

📑 DOCX

📊 Excel

📈 CSV

📝 TXT
""")

with col2:

    st.info("""
🤖 Gemini AI

🧠 FAISS

📚 RAG

💬 Chat Memory

⚡ Fast Search
""")

with col3:

    st.info("""
📥 Export PDF

📥 Export TXT

📥 Markdown

📊 Dashboard

☁ Streamlit Cloud
""")

# ===================================================
# FOOTER
# ===================================================

st.markdown("<br><br>",unsafe_allow_html=True)

st.markdown("---")

st.markdown(
"""
<div style="text-align:center">

<h3>🤖 RAG Chatbot Pro</h3>

Professional Retrieval-Augmented Generation Chatbot

Built with

<b>Streamlit • Gemini AI • FAISS • Sentence Transformers</b>

<br><br>

Made with ❤️ by <b>Siva Prasad</b>

</div>
""",
unsafe_allow_html=True
)
