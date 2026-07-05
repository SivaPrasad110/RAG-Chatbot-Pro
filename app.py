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

from export import (
    export_txt,
    export_markdown,
    export_pdf
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="RAG Chatbot Pro",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# SESSION STATE
# =====================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chunks" not in st.session_state:
    st.session_state.chunks = []

if "index" not in st.session_state:
    st.session_state.index = None

if "documents_loaded" not in st.session_state:
    st.session_state.documents_loaded = False

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

/* Main */

.stApp{

background:
radial-gradient(circle at center,
#172554 0%,
#111827 45%,
#0b0b0b 100%);

}

/* Remove Header */

header{

visibility:hidden;

}

/* Footer */

footer{

visibility:hidden;

}

/* Main Width */

.block-container{

max-width:1250px;

padding-top:2rem;

}

/* Sidebar */

section[data-testid="stSidebar"]{

background:#111827;

border-right:1px solid #222;

}

/* Sidebar text */

section[data-testid="stSidebar"] *{

color:white;

}

/* Buttons */

.stButton>button{

width:100%;

height:48px;

border-radius:15px;

background:#1F2937;

border:1px solid #374151;

color:white;

font-weight:600;

}

.stButton>button:hover{

background:#2563EB;

}

/* Chat input */

div[data-testid="stChatInput"]{

padding-top:20px;

}

/* Chat message */

.stChatMessage{

border-radius:18px;

padding:15px;

}

/* Suggestion Card */

.suggest{

background:#1E293B;

padding:12px;

border-radius:14px;

text-align:center;

font-weight:600;

border:1px solid #334155;

}

.suggest:hover{

background:#2563EB;

cursor:pointer;

}

/* Hero */

.hero{

text-align:center;

padding-top:40px;

padding-bottom:20px;

}

.hero h1{

font-size:60px;

font-weight:700;

margin-bottom:10px;

color:white;

}

.hero p{

font-size:22px;

color:#D1D5DB;

}

/* Footer */

.footer{

text-align:center;

color:#9CA3AF;

padding-top:60px;

}

</style>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown("## ✨ RAG Chatbot Pro")

    st.caption("Gemini Powered")

    st.markdown("---")

    if st.button("➕ New Chat"):

        st.session_state.messages=[]

        st.rerun()

    st.markdown("### 🕒 Recent Chats")

    st.caption("• AI Project")

    st.caption("• Final Report")

    st.caption("• Research Paper")

    st.caption("• Resume")

    st.markdown("---")

    st.subheader("📂 Upload Documents")

    uploaded_files=st.file_uploader(

        "",

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

    top_k=st.slider(
        "Retrieved Chunks",
        1,
        10,
        5
    )

    chunk_size=st.slider(
        "Chunk Size",
        200,
        1200,
        700,
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

    st.markdown("### 👤 Siva Prasad")

    st.caption("🟢 Gemini Connected")

# =====================================================
# HERO
# =====================================================

st.markdown("""

<div class="hero">

<h1>

Hello, Siva 👋

</h1>

<p>

How can I help you today?

</p>

</div>

""", unsafe_allow_html=True)

# =====================================================
# SUGGESTION BUTTONS
# =====================================================

c1,c2,c3=st.columns(3)

with c1:

    st.markdown(
        '<div class="suggest">📄 Summarize Document</div>',
        unsafe_allow_html=True
    )

with c2:

    st.markdown(
        '<div class="suggest">💡 Explain Concepts</div>',
        unsafe_allow_html=True
    )

with c3:

    st.markdown(
        '<div class="suggest">📊 Generate Insights</div>',
        unsafe_allow_html=True
    )

st.markdown("<br>",unsafe_allow_html=True)
# =====================================================
# AI PROMPT SECTION
# =====================================================

st.markdown("<br>", unsafe_allow_html=True)

container = st.container(border=True)

with container:

    st.markdown("""
    <h3 style="text-align:center;">
    💬 Ask AI Anything
    </h3>

    <p style="text-align:center;color:#9CA3AF;">
    Upload documents and ask questions using Retrieval-Augmented Generation.
    </p>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns([2,2,2,2])

    with c1:
        st.button(
            "📄 Summarize",
            use_container_width=True
        )

    with c2:
        st.button(
            "💡 Explain",
            use_container_width=True
        )

    with c3:
        st.button(
            "📊 Insights",
            use_container_width=True
        )

    with c4:
        st.button(
            "📑 Compare",
            use_container_width=True
        )

st.markdown("<br>", unsafe_allow_html=True)

# =====================================================
# CHAT INPUT
# =====================================================

question = st.chat_input(
    "Ask anything about your uploaded documents..."
)
# =====================================================
# CHAT CONVERSATION
# =====================================================

st.markdown("<br>", unsafe_allow_html=True)

chat_box = st.container(border=True)

with chat_box:

    st.markdown(
        """
        <h3 style='text-align:center;'>
        💬 Conversation
        </h3>
        """,
        unsafe_allow_html=True
    )

    # -----------------------------
    # Display Previous Messages
    # -----------------------------

    for message in st.session_state.messages:

        avatar = "👤" if message["role"] == "user" else "🤖"

        with st.chat_message(
            message["role"],
            avatar=avatar
        ):

            st.markdown(message["content"])

# =====================================================
# ASK QUESTION
# =====================================================

if st.session_state.documents_loaded:

    question = st.chat_input(
        "Ask anything about your uploaded documents..."
    )

    if question:

        # ------------------------------------
        # USER
        # ------------------------------------

        st.session_state.messages.append(
            {
                "role":"user",
                "content":question
            }
        )

        with st.chat_message(
            "user",
            avatar="👤"
        ):
            st.markdown(question)

        # ------------------------------------
        # SEARCH
        # ------------------------------------

        with st.spinner("🔍 Searching documents..."):

            results = search_chunks(

                question,

                st.session_state.chunks,

                st.session_state.index,

                top_k

            )

        # ------------------------------------
        # BUILD CONTEXT
        # ------------------------------------

        context = ""

        for item in results:

            context += f"""

Document : {item['source']}

Page : {item['page']}

Content :

{item['text']}

"""

        # ------------------------------------
        # AI RESPONSE
        # ------------------------------------

        with st.chat_message(
            "assistant",
            avatar="🤖"
        ):

            thinking = st.empty()

            thinking.info("🤖 Gemini is thinking...")

            answer = ask_gemini(

                question,

                context

            )

            thinking.empty()

            # Typing animation

            output = st.empty()

            text = ""

            for word in answer.split():

                text += word + " "

                output.markdown(text + "▌")

            output.markdown(answer)

        # ------------------------------------
        # SAVE CHAT
        # ------------------------------------

        st.session_state.messages.append(
            {
                "role":"assistant",
                "content":answer
            }
        )

else:

    st.info(
        """
👋 Welcome!

Upload documents from the left sidebar.

Then ask any question.

Supported files

• PDF

• DOCX

• TXT

• CSV

• Excel

Your answers are generated using
Gemini AI + FAISS + RAG.
"""
    )
# =====================================================
# SIDEBAR DASHBOARD
# =====================================================

with st.sidebar:

    st.markdown("---")

    st.subheader("📊 Workspace")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "📄 Docs",
            len(uploaded_files) if uploaded_files else 0
        )

    with col2:
        st.metric(
            "💬 Chat",
            len(st.session_state.messages)
        )

    st.metric(
        "🧠 Chunks",
        len(st.session_state.chunks)
    )

    if st.session_state.documents_loaded:

        st.success("🟢 AI Ready")

    else:

        st.warning("🟡 Upload Documents")

# =====================================================
# EXPORT
# =====================================================

    st.markdown("---")

    st.subheader("📥 Export")

    st.download_button(
        "📄 TXT",
        export_txt(
            st.session_state.messages
        ),
        "chat.txt",
        use_container_width=True
    )

    st.download_button(
        "📝 Markdown",
        export_markdown(
            st.session_state.messages
        ),
        "chat.md",
        use_container_width=True
    )

    if st.button(
        "📕 Generate PDF",
        use_container_width=True
    ):

        pdf_path = export_pdf(
            st.session_state.messages
        )

        with open(
            pdf_path,
            "rb"
        ) as pdf:

            st.download_button(

                "⬇ Download PDF",

                pdf,

                "chat.pdf",

                use_container_width=True

            )

# =====================================================
# QUICK ACTIONS
# =====================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("### ⚡ Quick Actions")

col1,col2,col3,col4=st.columns(4)

with col1:

    if st.button(
        "📄 Summarize",
        use_container_width=True
    ):
        st.info("Ask AI to summarize your uploaded document.")

with col2:

    if st.button(
        "💡 Explain",
        use_container_width=True
    ):
        st.info("Ask AI to explain any topic.")

with col3:

    if st.button(
        "📊 Insights",
        use_container_width=True
    ):
        st.info("Generate key insights from the document.")

with col4:

    if st.button(
        "📑 Compare",
        use_container_width=True
    ):
        st.info("Compare two uploaded documents.")

# =====================================================
# ABOUT
# =====================================================

with st.expander(
    "🚀 About RAG Chatbot Pro",
    expanded=False
):

    st.markdown("""

### 🤖 RAG Chatbot Pro

Professional AI-powered document assistant.

### Features

- 📄 PDF
- 📑 DOCX
- 📊 Excel
- 📈 CSV
- 📝 TXT
- 🔍 FAISS Search
- 🤖 Gemini AI
- 💬 Chat Memory
- 📥 Export Chat
- ⚡ Streamlit

""")

# =====================================================
# FOOTER
# =====================================================

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("---")

st.markdown(
"""
<div style="text-align:center">

<h3>🤖 RAG Chatbot Pro</h3>

<p>

Powered by

<b>Gemini AI • FAISS • Sentence Transformers</b>

</p>

</div>
""",
unsafe_allow_html=True
)
