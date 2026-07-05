import streamlit as st


def sidebar():

    with st.sidebar:

        st.markdown(
            """
            <h2 style='text-align:center;'>
            🤖 RAG Chatbot Pro
            </h2>
            """,
            unsafe_allow_html=True
        )

        st.caption(
            "Gemini Powered AI Assistant"
        )

        st.markdown("---")

        # ===========================
        # NEW CHAT
        # ===========================

        if st.button(
            "➕ New Chat",
            use_container_width=True,
            key="new_chat"
        ):

            st.session_state.messages = []

            st.rerun()

        st.markdown("---")

        # ===========================
        # DOCUMENT UPLOAD
        # ===========================

        st.subheader("📂 Upload Documents")

        uploaded_files = st.file_uploader(

            "Choose files",

            type=[
                "pdf",
                "docx",
                "txt",
                "csv",
                "xlsx"
            ],

            accept_multiple_files=True,

            key="document_upload"

        )

        if uploaded_files:

            st.success(
                f"{len(uploaded_files)} file(s) selected"
            )

            with st.expander(
                "📄 Uploaded Files",
                expanded=False
            ):

                for file in uploaded_files:

                    st.write(
                        f"✅ {file.name}"
                    )

        st.markdown("---")

        # ===========================
        # AI SETTINGS
        # ===========================

        st.subheader("⚙️ AI Settings")

        top_k = st.slider(

            "Retrieved Chunks",

            min_value=1,

            max_value=10,

            value=5,

            key="top_k"

        )

        chunk_size = st.slider(

            "Chunk Size",

            min_value=200,

            max_value=1200,

            value=600,

            step=100,

            key="chunk_size"

        )

        overlap = st.slider(

            "Chunk Overlap",

            min_value=0,

            max_value=300,

            value=100,

            step=20,

            key="chunk_overlap"

        )

        st.markdown("---")

        # ===========================
        # DASHBOARD
        # ===========================

        st.subheader("📊 Dashboard")

        st.metric(

            "💬 Messages",

            len(
                st.session_state.messages
            )

        )

        st.metric(

            "📚 Chunks",

            len(
                st.session_state.chunks
            )

        )

        if st.session_state.documents_loaded:

            st.success(
                "🟢 AI Ready"
            )

        else:

            st.warning(
                "🟡 Waiting for Documents"
            )

        st.markdown("---")

        # ===========================
        # QUICK ACTIONS
        # ===========================

        st.subheader("⚡ Quick Actions")

        if st.button(
            "🗑 Clear Chat",
            use_container_width=True,
            key="clear_chat"
        ):

            st.session_state.messages = []

            st.rerun()

        st.button(
            "📊 Analytics",
            use_container_width=True,
            disabled=True,
            key="analytics"
        )

        st.button(
            "📥 Export",
            use_container_width=True,
            disabled=True,
            key="export"
        )

        st.markdown("---")

        # ===========================
        # USER
        # ===========================

        st.markdown(
            """
            <div style='text-align:center;'>

            <h4>👤 Siva Prasad</h4>

            🟢 Gemini Connected

            </div>
            """,
            unsafe_allow_html=True
        )

    return {

        "uploaded_files": uploaded_files,

        "top_k": top_k,

        "chunk_size": chunk_size,

        "overlap": overlap

    }
