import streamlit as st

def load_css():

    st.markdown("""
<style>

/* =====================================================
GLOBAL
===================================================== */

html, body, [class*="css"] {

    font-family: "Segoe UI", sans-serif;

}

/* =====================================================
APP BACKGROUND
===================================================== */

.stApp{

    background:
    radial-gradient(circle at top,
    #1e3a8a 0%,
    #111827 45%,
    #0f172a 100%);

}

/* =====================================================
HEADER
===================================================== */

.main-title{

    text-align:center;

    color:white;

    font-size:55px;

    font-weight:700;

    margin-bottom:10px;

}

.sub-title{

    text-align:center;

    color:#d1d5db;

    font-size:20px;

    margin-bottom:30px;

}

/* =====================================================
SIDEBAR
===================================================== */

section[data-testid="stSidebar"]{

    background:#111827;

    border-right:1px solid #374151;

}

section[data-testid="stSidebar"] *{

    color:white;

}

/* =====================================================
CARDS
===================================================== */

.card{

    background:#1E293B;

    padding:20px;

    border-radius:16px;

    border:1px solid #334155;

    margin-bottom:15px;

}

/* =====================================================
METRICS
===================================================== */

[data-testid="metric-container"]{

    background:#1E293B;

    border-radius:15px;

    padding:18px;

    border:1px solid #334155;

}

/* =====================================================
CHAT
===================================================== */

.stChatMessage{

    border-radius:18px;

    padding:16px;

    margin-top:10px;

    margin-bottom:10px;

    border:1px solid rgba(255,255,255,.05);

}

/* =====================================================
CHAT INPUT
===================================================== */

div[data-testid="stChatInput"]{

    margin-top:20px;

}

/* =====================================================
BUTTONS
===================================================== */

.stButton>button{

    width:100%;

    border-radius:12px;

    height:45px;

    background:#2563EB;

    color:white;

    border:none;

    transition:.3s;

}

.stButton>button:hover{

    background:#1D4ED8;

    transform:scale(1.02);

}

/* =====================================================
DOWNLOAD BUTTON
===================================================== */

.stDownloadButton>button{

    width:100%;

    border-radius:12px;

}

/* =====================================================
FILE UPLOADER
===================================================== */

[data-testid="stFileUploader"]{

    border-radius:16px;

}

/* =====================================================
EXPANDER
===================================================== */

.streamlit-expanderHeader{

    font-size:18px;

    font-weight:600;

}

/* =====================================================
SCROLLBAR
===================================================== */

::-webkit-scrollbar{

    width:8px;

}

::-webkit-scrollbar-thumb{

    background:#4B5563;

    border-radius:10px;

}

/* =====================================================
ANIMATION
===================================================== */

.stChatMessage{

    animation:fadeIn .35s ease;

}

@keyframes fadeIn{

    from{

        opacity:0;

        transform:translateY(10px);

    }

    to{

        opacity:1;

        transform:translateY(0);

    }

}

/* =====================================================
FOOTER
===================================================== */

footer{

    visibility:hidden;

}

header{

    visibility:hidden;

}

</style>
""", unsafe_allow_html=True)
