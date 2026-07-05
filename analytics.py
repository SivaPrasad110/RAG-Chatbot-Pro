"""
analytics.py
Analytics Dashboard
"""

import streamlit as st


def show_dashboard(messages, chunks):

    st.header("📊 Analytics Dashboard")

    total_questions = len(
        [
            m
            for m in messages
            if m["role"] == "user"
        ]
    )

    total_answers = len(
        [
            m
            for m in messages
            if m["role"] == "assistant"
        ]
    )

    total_chunks = len(chunks)

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Questions",
        total_questions
    )

    col2.metric(
        "Answers",
        total_answers
    )

    col3.metric(
        "Chunks",
        total_chunks
    )

    st.divider()

    st.subheader("Conversation")

    for msg in messages:

        st.write(
            f"**{msg['role'].capitalize()}** : {msg['content']}"
        )