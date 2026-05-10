import streamlit as st

# =========================================================
# LOAD CSS
# =========================================================

def load_css():

    st.markdown("""

    <style>

    /* =====================================================
    GOOGLE FONT
    ===================================================== */

    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800&display=swap');

    /* =====================================================
    ROOT
    ===================================================== */

    :root {

        --primary: #2563eb;

        --primary-soft: #dbeafe;

        --secondary: #7c3aed;

        --success: #10b981;

        --danger: #ef4444;

        --warning: #f59e0b;

        --bg-main: #eef4ff;

        --bg-card: rgba(255,255,255,0.75);

        --border: rgba(255,255,255,0.45);

        --text-main: #0f172a;

        --text-soft: #64748b;

        --shadow:
            0 10px 35px rgba(15,23,42,0.08);

        --radius: 22px;
    }

    /* =====================================================
    PAGE
    ===================================================== */

    html,
    body,
    .stApp {

        direction: rtl !important;

        text-align: right !important;

        font-family:
            'Tajawal',
            sans-serif;

        color:
            var(--text-main);

        background:
            linear-gradient(
                135deg,
                #eef4ff 0%,
                #f8fbff 40%,
                #edf7ff 100%
            );
    }

    /* =====================================================
    BACKGROUND SHAPES
    ===================================================== */

    .stApp::before {

        content: "";

        position: fixed;

        width: 500px;

        height: 500px;

        background:
            rgba(37,99,235,0.10);

        border-radius: 50%;

        top: -200px;

        right: -120px;

        filter: blur(40px);

        z-index: 0;
    }

    .stApp::after {

        content: "";

        position: fixed;

        width: 400px;

        height: 400px;

        background:
            rgba(124,58,237,0.08);

        border-radius: 50%;

        bottom: -180px;

        left: -100px;

        filter: blur(40px);

        z-index: 0;
    }

    /* =====================================================
    MAIN CONTAINER
    ===================================================== */

    .block-container {

        position: relative;

        z-index: 1;

        padding-top: 5rem;

        padding-bottom: 2rem;

        max-width: 96%;
    }

    /* =====================================================
    HEADER
    ===================================================== */

    header {

        background:
            rgba(255,255,255,0.60) !important;

        backdrop-filter:
            blur(16px);

        border-bottom:
            1px solid rgba(255,255,255,0.25);
    }

    /* =====================================================
    SIDEBAR
    ===================================================== */

    section[data-testid="stSidebar"] {

        background:
            rgba(255,255,255,0.60);

        backdrop-filter:
            blur(18px);

        border-left:
            1px solid rgba(255,255,255,0.30);
    }

    section[data-testid="stSidebar"] * {

        direction: rtl !important;

        text-align: right !important;
    }

    /* =====================================================
    TABS
    ===================================================== */

    .stTabs {

        direction: rtl !important;
    }

    div[data-baseweb="tab-list"] {

        gap: 12px;

        overflow-x: auto;

        padding-bottom: 16px;
    }

    button[data-baseweb="tab"] {

        background:
            rgba(255,255,255,0.65);

        backdrop-filter:
            blur(14px);

        border:
            1px solid rgba(255,255,255,0.45);

        border-radius:
            18px;

        padding:
            12px 24px;

        min-width:
            180px;

        height:
            58px;

        font-size:
            15px;

        font-weight:
            700;

        color:
            var(--text-main);

        transition:
            0.25s;

        box-shadow:
            0 4px 18px rgba(15,23,42,0.04);
    }

    button[data-baseweb="tab"]:hover {

        transform:
            translateY(-2px);

        background:
            rgba(255,255,255,0.88);
    }

    button[aria-selected="true"] {

        background:
            linear-gradient(
                135deg,
                #2563eb,
                #4f46e5
            ) !important;

        color:
            white !important;

        box-shadow:
            0 10px 30px rgba(37,99,235,0.25);
    }

    /* =====================================================
    CARDS
    ===================================================== */

    .card {

        background:
            rgba(255,255,255,0.65);

        backdrop-filter:
            blur(18px);

        border:
            1px solid rgba(255,255,255,0.45);

        border-radius:
            var(--radius);

        padding:
            26px;

        margin-bottom:
            22px;

        box-shadow:
            var(--shadow);
    }

    .card-title {

        font-size:
            24px;

        font-weight:
            800;

        margin-bottom:
            20px;

        color:
            var(--text-main);
    }

    /* =====================================================
    METRICS
    ===================================================== */

    div[data-testid="metric-container"] {

        background:
            rgba(255,255,255,0.70);

        backdrop-filter:
            blur(18px);

        border:
            1px solid rgba(255,255,255,0.50);

        border-radius:
            24px;

        padding:
            18px;

        box-shadow:
            0 8px 28px rgba(15,23,42,0.05);

        transition:
            0.25s;
    }

    div[data-testid="metric-container"]:hover {

        transform:
            translateY(-3px);

        box-shadow:
            0 12px 32px rgba(15,23,42,0.08);
    }

    div[data-testid="metric-container"] label {

        color:
            var(--text-soft) !important;

        font-weight:
            700 !important;
    }

    div[data-testid="metric-container"] [data-testid="stMetricValue"] {

        color:
            var(--text-main) !important;

        font-weight:
            800;
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
            rgba(255,255,255,0.90) !important;

        border:
            1px solid rgba(255,255,255,0.55) !important;

        border-radius:
            18px !important;

        color:
            var(--text-main) !important;

        min-height:
            52px !important;

        text-align:
            right !important;

        box-shadow:
            inset 0 2px 4px rgba(15,23,42,0.02);
    }

    textarea {

        min-height:
            120px !important;
    }

    /* =====================================================
    BUTTONS
    ===================================================== */

    .stButton button,
    .stDownloadButton button {

        border:
            none;

        border-radius:
            18px;

        height:
            54px;

        font-size:
            15px;

        font-weight:
            800;

        color:
            white;

        background:
            linear-gradient(
                135deg,
                #2563eb,
                #4f46e5
            );

        box-shadow:
            0 10px 25px rgba(37,99,235,0.25);

        transition:
            0.25s;
    }

    .stButton button:hover,
    .stDownloadButton button:hover {

        transform:
            translateY(-2px);

        box-shadow:
            0 14px 32px rgba(37,99,235,0.30);
    }

    /* =====================================================
    FILE UPLOADER
    ===================================================== */

    section[data-testid="stFileUploader"] {

        background:
            rgba(255,255,255,0.65);

        backdrop-filter:
            blur(18px);

        border:
            2px dashed rgba(37,99,235,0.18);

        border-radius:
            24px;

        padding:
            24px;

        box-shadow:
            var(--shadow);
    }

    /* =====================================================
    DATAFRAME
    ===================================================== */

    .stDataFrame {

        border-radius:
            24px;

        overflow:
            hidden;

        border:
            1px solid rgba(255,255,255,0.40);

        box-shadow:
            var(--shadow);
    }

    .stDataFrame table {

        direction:
            rtl !important;
    }

    .stDataFrame th {

        background:
            rgba(219,234,254,0.90) !important;

        color:
            #1e3a8a !important;

        font-weight:
            800 !important;

        text-align:
            right !important;
    }

    .stDataFrame td {

        text-align:
            right !important;
    }

    /* =====================================================
    ALERTS
    ===================================================== */

    .stAlert {

        border-radius:
            18px;

        border:
            none;

        box-shadow:
            var(--shadow);
    }

    /* =====================================================
    SCROLLBAR
    ===================================================== */

    ::-webkit-scrollbar {

        width:
            10px;

        height:
            10px;
    }

    ::-webkit-scrollbar-thumb {

        background:
            #cbd5e1;

        border-radius:
            20px;
    }

    ::-webkit-scrollbar-track {

        background:
            transparent;
    }

    /* =====================================================
    MOBILE
    ===================================================== */

    @media (max-width: 768px) {

        .block-container {

            padding-top:
                3rem;

            max-width:
                100%;
        }

        .card {

            padding:
                18px;
        }

        button[data-baseweb="tab"] {

            min-width:
                140px;

            font-size:
                13px;
        }
    }

    </style>

    """, unsafe_allow_html=True)
