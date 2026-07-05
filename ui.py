import streamlit as st
import time

# =====================================================
# HERO SECTION
# =====================================================

def hero_section():

    st.markdown(
        """
        <div class="hero">

            <h1 class="main-title">

                🤖 RAG Chatbot Pro

            </h1>

            <p class="sub-title">

                Hello, Siva 👋

            </p>

            <p style="text-align:center;color:#94A3B8;font-size:18px;">

                How can I help you today?

            </p>

        </div>
        """,
        unsafe_allow_html=True
    )


# =====================================================
# SUGGESTION CARDS
# =====================================================

def suggestion_cards():

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            <div class="card">

            <h4>📄 Summarize</h4>

            Summarize uploaded documents instantly.

            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
            <div class="card">

            <h4>💡 Explain</h4>

            Explain difficult concepts in simple words.

            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            """
            <div class="card">

            <h4>📊 Generate Insights</h4>

            Discover key information from your documents.

            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)


# =====================================================
# WELCOME SCREEN
# =====================================================

def welcome_screen():

    st.info(
        """
👋 Welcome!

Upload your documents from the sidebar.

Supported formats

• PDF

• DOCX

• TXT

• CSV

• Excel

Then start chatting with your AI assistant.
"""
    )
# =====================================================
# CHAT INTERFACE
# =====================================================

def chat_interface(

    chunks,

    index,

    top_k,

    search_function,

    llm_function

):

    # ------------------------------------
    # Display Previous Messages
    # ------------------------------------

    for message in st.session_state.messages:

        avatar = "👤" if message["role"] == "user" else "🤖"

        with st.chat_message(

            message["role"],

            avatar=avatar

        ):

            st.markdown(

                message["content"]

            )

    # ------------------------------------
    # Chat Input
    # ------------------------------------

    question = st.chat_input(

        "💬 Ask anything about your documents..."

    )

    if not question:

        return None

    # ------------------------------------
    # USER MESSAGE
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
    # SEARCH DOCUMENTS
    # ------------------------------------

    with st.spinner(

        "🔍 Searching documents..."

    ):

        results = search_function(

            question,

            chunks,

            index,

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
    # GEMINI RESPONSE
    # ------------------------------------

    with st.chat_message(

        "assistant",

        avatar="🤖"

    ):

        thinking = st.empty()

        thinking.info(

            "🤖 Gemini is thinking..."

        )

        answer = llm_function(

            question,

            context

        )

        thinking.empty()

        # -----------------------------
        # Typing Animation
        # -----------------------------

        output = st.empty()

        sentence = ""

        for word in answer.split():

            sentence += word + " "

            output.markdown(

                sentence + "▌"

            )

            time.sleep(0.02)

        output.markdown(answer)

    # ------------------------------------
    # SAVE ANSWER
    # ------------------------------------

    st.session_state.messages.append(

        {

            "role":"assistant",

            "content":answer

        }

    )

    return answer
# =====================================================
# CONVERSATION STATS
# =====================================================

def conversation_stats():

    total = len(st.session_state.messages)

    user = len(
        [
            m for m in st.session_state.messages
            if m["role"] == "user"
        ]
    )

    assistant = len(
        [
            m for m in st.session_state.messages
            if m["role"] == "assistant"
        ]
    )

    st.markdown("---")

    st.subheader("📊 Conversation")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Messages",
            total
        )

    with c2:
        st.metric(
            "User",
            user
        )

    with c3:
        st.metric(
            "AI",
            assistant
        )


# =====================================================
# LOADING SCREEN
# =====================================================

def loading_screen():

    with st.spinner(
        "🤖 Gemini is preparing..."
    ):

        time.sleep(1)


# =====================================================
# EMPTY CHAT
# =====================================================

def empty_chat():

    st.markdown(
        """
<div style="

background:#111827;

padding:40px;

border-radius:20px;

text-align:center;

border:1px solid #334155;

">

<h2>

👋 Welcome

</h2>

<p>

Upload your documents and start chatting.

</p>

</div>

""",
        unsafe_allow_html=True
    )


# =====================================================
# AI STATUS
# =====================================================

def ai_status():

    if st.session_state.documents_loaded:

        st.success(
            "🟢 AI Ready"
        )

    else:

        st.warning(
            "🟡 Waiting for documents..."
        )


# =====================================================
# FOOTER
# =====================================================

def footer():

    st.markdown("---")

    st.markdown(
        """
<div style="

text-align:center;

padding:20px;

color:#9CA3AF;

">

<h3>

🤖 RAG Chatbot Pro

</h3>

<p>

Powered by

<b>

Gemini AI • FAISS • Sentence Transformers

</b>

</p>

<p>

Made with ❤️ by Siva Prasad

</p>

</div>
""",
        unsafe_allow_html=True
    )
