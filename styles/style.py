import streamlit as st

# =========================================================
# LOAD CSS
# =========================================================

def load_css():

    st.markdown("""

    <style>

    /* =====================================================
       GLOBAL
    ===================================================== */

    html, body, .stApp {

        direction: rtl;

        text-align: right;

        font-family:
            "Segoe UI",
            Tahoma,
            sans-serif;
    }

    .stApp {

        background:
            linear-gradient(
                180deg,
                #020617 0%,
                #071226 100%
            );

        color: #f8fafc;
    }

    /* =====================================================
       MAIN CONTAINER
    ===================================================== */

    .block-container {

        padding-top: 1rem;

        padding-bottom: 2rem;

        max-width: 100%;
    }

    /* =====================================================
       REMOVE OVERLAYS
    ===================================================== */

    div[data-baseweb="dialog"] {

        background: transparent !important;
    }

    div[role="dialog"] {

        background: transparent !important;

        box-shadow: none !important;
    }

    /* =====================================================
       CARDS
    ===================================================== */

    .card {

        background:
            linear-gradient(
                145deg,
                #0f172a,
                #162033
            );

        border-radius: 22px;

        padding: 24px;

        margin-bottom: 18px;

        border: 1px solid rgba(255,255,255,0.06);

        box-shadow:
            0 10px 30px rgba(0,0,0,0.25);
    }

    .card-title {

        font-size: 24px;

        font-weight: 700;

        margin-bottom: 20px;

        color: #ffffff;
    }

    /* =====================================================
       BUTTONS
    ===================================================== */

    .stButton button,
    .stDownloadButton button {

        width: 100%;

        border-radius: 14px;

        border: none;

        padding: 12px 18px;

        font-weight: bold;

        color: white;

        background:
            linear-gradient(
                135deg,
                #2563eb,
                #4338ca
            );

        transition: 0.3s;
    }

    .stButton button:hover,
    .stDownloadButton button:hover {

        transform: translateY(-1px);

        background:
            linear-gradient(
                135deg,
                #1d4ed8,
                #312e81
            );
    }

    /* =====================================================
       INPUTS
    ===================================================== */

    .stTextInput input,
    .stDateInput input,
    .stTextArea textarea,
    .stNumberInput input {

        background-color: #0f172a !important;

        color: white !important;

        border-radius: 12px !important;

        border: 1px solid rgba(255,255,255,0.08) !important;
    }

    div[data-baseweb="select"] > div {

        background-color: #0f172a !important;

        color: white !important;

        border-radius: 12px !important;
    }

    /* =====================================================
       TABS
    ===================================================== */

    button[data-baseweb="tab"] {

        font-size: 16px;

        font-weight: 700;

        border-radius: 12px;

        padding: 10px 18px;

        margin-left: 6px;

        background: #0f172a;

        color: white;
    }

    button[data-baseweb="tab"][aria-selected="true"] {

        background:
            linear-gradient(
                135deg,
                #2563eb,
                #4338ca
            ) !important;

        color: white !important;
    }

    /* =====================================================
       DATAFRAME
    ===================================================== */

    .stDataFrame {

        border-radius: 16px;

        overflow: hidden;

        border: 1px solid rgba(255,255,255,0.08);
    }

    /* =====================================================
       KPI
    ===================================================== */

    div[data-testid="metric-container"] {

        background:
            linear-gradient(
                145deg,
                #0f172a,
                #162033
            );

        border-radius: 18px;

        padding: 16px;

        border: 1px solid rgba(255,255,255,0.06);

        box-shadow:
            0 4px 18px rgba(0,0,0,0.18);
    }

    /* =====================================================
       SIDEBAR
    ===================================================== */

    section[data-testid="stSidebar"] {

        background:
            linear-gradient(
                180deg,
                #0f172a,
                #111c30
            );
    }

    /* =====================================================
       ALERTS
    ===================================================== */

    .stAlert {

        border-radius: 14px;
    }

    /* =====================================================
       HIDE STREAMLIT MENU
    ===================================================== */

    #MainMenu {

        visibility: hidden;
    }

    footer {

        visibility: hidden;
    }

    header {

        visibility: hidden;
    }

    </style>

    """, unsafe_allow_html=True)
