import streamlit as st

# =========================================================
# LOAD CSS
# =========================================================

def load_css():

    st.markdown("""

    <style>

    /* =====================================================
    ROOT
    ===================================================== */

    :root {

        --bg-main: #020817;

        --bg-card: #0f172a;

        --bg-card-2: #111c34;

        --border-color: rgba(255,255,255,0.07);

        --primary: #2563eb;

        --primary-hover: #1d4ed8;

        --text-main: #f8fafc;

        --text-soft: #cbd5e1;
    }

    /* =====================================================
    PAGE
    ===================================================== */

    html,
    body,
    .stApp {

        direction: rtl;

        text-align: right;

        font-family:
            "Segoe UI",
            Tahoma,
            sans-serif;

        background-color: var(--bg-main);

        color: var(--text-main);
    }

    .stApp {

        background:
            linear-gradient(
                180deg,
                #020617 0%,
                #071226 100%
            );
    }

    /* =====================================================
    MAIN CONTAINER
    ===================================================== */

    .block-container {

        padding-top: 5rem;

        padding-bottom: 2rem;

        max-width: 98%;

        margin: auto;
    }

    /* =====================================================
    TOP HEADER FIX
    ===================================================== */

    header {

        background:
            rgba(2,6,23,0.75) !important;

        backdrop-filter: blur(10px);
    }

    /* =====================================================
    TABS FIX
    ===================================================== */

    .stTabs {

        direction: ltr;

        margin-top: 10px;
    }

    .stTabs > div {

        direction: rtl;
    }

    div[data-baseweb="tab-list"] {

        gap: 12px;

        justify-content: flex-start;

        overflow-x: auto;

        flex-wrap: nowrap;

        padding:

            12px
            0
            16px
            0;
    }

    button[data-baseweb="tab"] {

        height: 54px;

        border-radius: 14px;

        padding:
            10px
            24px;

        font-size: 16px;

        font-weight: 700;

        color: white;

        background:
            rgba(15,23,42,0.95);

        border:
            1px solid var(--border-color);

        transition: 0.25s;

        min-width: 190px;
    }

    button[data-baseweb="tab"]:hover {

        background:
            rgba(37,99,235,0.15);

        border-color:
            rgba(37,99,235,0.4);
    }

    button[aria-selected="true"] {

        background:
            linear-gradient(
                135deg,
                #2563eb,
                #1d4ed8
            ) !important;

        color: white !important;

        box-shadow:
            0 4px 18px rgba(37,99,235,0.35);
    }

    /* =====================================================
    CARDS
    ===================================================== */

    .card {

        background:
            linear-gradient(
                180deg,
                rgba(15,23,42,0.98),
                rgba(17,28,52,0.98)
            );

        border-radius: 22px;

        padding: 24px;

        margin-bottom: 18px;

        border:
            1px solid var(--border-color);

        box-shadow:
            0 10px 30px rgba(0,0,0,0.22);
    }

    .card-title {

        font-size: 24px;

        font-weight: 800;

        margin-bottom: 18px;

        color: white;
    }

    /* =====================================================
    METRICS
    ===================================================== */

    div[data-testid="metric-container"] {

        background:
            linear-gradient(
                180deg,
                rgba(15,23,42,0.98),
                rgba(17,28,52,0.98)
            );

        border-radius: 18px;

        padding: 16px;

        border:
            1px solid var(--border-color);

        box-shadow:
            0 4px 16px rgba(0,0,0,0.16);
    }

    div[data-testid="metric-container"] label {

        color: var(--text-soft) !important;
    }

    /* =====================================================
    INPUTS
    ===================================================== */

    .stTextInput input,
    .stDateInput input,
    .stTextArea textarea,
    .stNumberInput input,
    .stSelectbox div[data-baseweb="select"] {

        background:
            rgba(2,6,23,0.95) !important;

        color:
            white !important;

        border-radius:
            14px !important;

        border:
            1px solid rgba(255,255,255,0.08) !important;

        min-height:
            48px !important;
    }

    textarea {

        min-height: 120px !important;
    }

    /* =====================================================
    BUTTONS
    ===================================================== */

    .stButton button,
    .stDownloadButton button {

        width: 100%;

        height: 52px;

        border-radius: 14px;

        border: none;

        font-size: 15px;

        font-weight: 700;

        background:
            linear-gradient(
                135deg,
                #2563eb,
                #1d4ed8
            );

        color: white;

        transition: 0.25s;

        box-shadow:
            0 4px 18px rgba(37,99,235,0.35);
    }

    .stButton button:hover,
    .stDownloadButton button:hover {

        transform:
            translateY(-1px);

        background:
            linear-gradient(
                135deg,
                #1d4ed8,
                #1e40af
            );
    }

    /* =====================================================
    FILE UPLOADER
    ===================================================== */

    section[data-testid="stFileUploader"] {

        background:
            rgba(15,23,42,0.92);

        border-radius: 18px;

        padding: 18px;

        border:
            1px dashed rgba(255,255,255,0.14);
    }

    /* =====================================================
    DATAFRAME
    ===================================================== */

    .stDataFrame {

        border-radius: 18px;

        overflow: hidden;

        border:
            1px solid rgba(255,255,255,0.08);
    }

    /* =====================================================
    ALERTS
    ===================================================== */

    .stAlert {

        border-radius: 14px;
    }

    /* =====================================================
    LABELS
    ===================================================== */

    label,
    .stMarkdown,
    p,
    span {

        color: var(--text-main);
    }

    /* =====================================================
    SCROLLBAR
    ===================================================== */

    ::-webkit-scrollbar {

        width: 10px;

        height: 10px;
    }

    ::-webkit-scrollbar-thumb {

        background: #334155;

        border-radius: 20px;
    }

    ::-webkit-scrollbar-track {

        background: transparent;
    }

    </style>

    """, unsafe_allow_html=True)