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

        --bg-main: #f4f7fb;

        --bg-card: #ffffff;

        --bg-card-2: #f8fafc;

        --border-color: rgba(15,23,42,0.08);

        --primary: #3b82f6;

        --primary-hover: #2563eb;

        --secondary: #6366f1;

        --success: #10b981;

        --danger: #ef4444;

        --warning: #f59e0b;

        --text-main: #0f172a;

        --text-soft: #64748b;

        --shadow:
            0 10px 30px rgba(15,23,42,0.06);
    }

    /* =====================================================
    PAGE RTL
    ===================================================== */

    html,
    body,
    .stApp {

        direction: rtl !important;

        text-align: right !important;

        font-family:
            "Segoe UI",
            Tahoma,
            sans-serif;

        background-color:
            var(--bg-main);

        color:
            var(--text-main);
    }

    .stApp {

        background:
            linear-gradient(
                180deg,
                #f8fbff 0%,
                #eef4ff 100%
            );
    }

    /* =====================================================
    FORCE RTL
    ===================================================== */

    * {

        direction: rtl;
    }

    .element-container,
    .stMarkdown,
    .stText,
    p,
    span,
    div,
    label {

        text-align: right !important;
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
    HEADER
    ===================================================== */

    header {

        background:
            rgba(255,255,255,0.88) !important;

        backdrop-filter:
            blur(12px);

        border-bottom:
            1px solid rgba(15,23,42,0.05);
    }

    /* =====================================================
    SIDEBAR
    ===================================================== */

    section[data-testid="stSidebar"] {

        background:
            linear-gradient(
                180deg,
                #ffffff,
                #f8fafc
            );

        border-left:
            1px solid rgba(15,23,42,0.05);
    }

    section[data-testid="stSidebar"] * {

        direction: rtl !important;

        text-align: right !important;
    }

    /* =====================================================
    TABS RTL
    ===================================================== */

    .stTabs {

        direction: rtl !important;

        margin-top: 12px;
    }

    .stTabs > div {

        direction: rtl !important;
    }

    div[data-baseweb="tab-list"] {

        direction: rtl !important;

        display: flex;

        justify-content: flex-start;

        gap: 12px;

        overflow-x: auto;

        flex-wrap: nowrap;

        padding:
            10px
            0
            18px
            0;
    }

    button[data-baseweb="tab"] {

        height: 54px;

        border-radius: 16px;

        padding:
            10px
            24px;

        font-size: 15px;

        font-weight: 700;

        color: #0f172a;

        background:
            rgba(255,255,255,0.95);

        border:
            1px solid rgba(15,23,42,0.06);

        transition: 0.25s;

        min-width: 190px;

        box-shadow:
            0 2px 10px rgba(15,23,42,0.04);
    }

    button[data-baseweb="tab"]:hover {

        transform:
            translateY(-1px);

        background:
            rgba(59,130,246,0.08);

        border-color:
            rgba(59,130,246,0.25);
    }

    button[aria-selected="true"] {

        background:
            linear-gradient(
                135deg,
                #3b82f6,
                #2563eb
            ) !important;

        color: white !important;

        box-shadow:
            0 6px 22px rgba(37,99,235,0.22);
    }

    /* =====================================================
    CARDS
    ===================================================== */

    .card {

        background:
            linear-gradient(
                180deg,
                #ffffff,
                #f8fafc
            );

        border-radius: 24px;

        padding: 24px;

        margin-bottom: 20px;

        border:
            1px solid rgba(15,23,42,0.06);

        box-shadow:
            var(--shadow);
    }

    .card-title {

        font-size: 24px;

        font-weight: 800;

        margin-bottom: 18px;

        color: #0f172a;

        text-align: right;
    }

    /* =====================================================
    METRICS
    ===================================================== */

    div[data-testid="metric-container"] {

        background:
            linear-gradient(
                180deg,
                #ffffff,
                #f8fafc
            );

        border-radius: 20px;

        padding: 18px;

        border:
            1px solid rgba(15,23,42,0.06);

        box-shadow:
            0 4px 16px rgba(15,23,42,0.05);

        transition: 0.25s;
    }

    div[data-testid="metric-container"]:hover {

        transform:
            translateY(-2px);

        box-shadow:
            0 10px 28px rgba(15,23,42,0.08);
    }

    div[data-testid="metric-container"] label {

        color:
            var(--text-soft) !important;

        font-weight: 600 !important;
    }

    div[data-testid="metric-container"] [data-testid="stMetricValue"] {

        color:
            #0f172a !important;

        font-weight: 800;
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
            white !important;

        color:
            #0f172a !important;

        border-radius:
            16px !important;

        border:
            1px solid rgba(15,23,42,0.08) !important;

        min-height:
            50px !important;

        text-align:
            right !important;

        box-shadow:
            inset 0 1px 3px rgba(15,23,42,0.03);
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

        width: 100%;

        height: 52px;

        border-radius: 16px;

        border: none;

        font-size: 15px;

        font-weight: 700;

        background:
            linear-gradient(
                135deg,
                #3b82f6,
                #2563eb
            );

        color: white;

        transition: 0.25s;

        box-shadow:
            0 6px 22px rgba(37,99,235,0.22);
    }

    .stButton button:hover,
    .stDownloadButton button:hover {

        transform:
            translateY(-2px);

        background:
            linear-gradient(
                135deg,
                #2563eb,
                #1d4ed8
            );

        box-shadow:
            0 10px 28px rgba(37,99,235,0.28);
    }

    /* =====================================================
    FILE UPLOADER
    ===================================================== */

    section[data-testid="stFileUploader"] {

        background:
            linear-gradient(
                180deg,
                #ffffff,
                #f8fafc
            );

        border-radius: 20px;

        padding: 20px;

        border:
            2px dashed rgba(59,130,246,0.18);

        box-shadow:
            var(--shadow);
    }

    /* =====================================================
    DATAFRAME RTL
    ===================================================== */

    .stDataFrame {

        border-radius: 20px;

        overflow: hidden;

        border:
            1px solid rgba(15,23,42,0.06);

        box-shadow:
            var(--shadow);
    }

    .stDataFrame table {

        direction: rtl !important;
    }

    .stDataFrame th {

        text-align: right !important;

        background:
            #eff6ff !important;

        color:
            #1e3a8a !important;
    }

    .stDataFrame td {

        text-align: right !important;
    }

    /* =====================================================
    ALERTS
    ===================================================== */

    .stAlert {

        border-radius: 16px;

        border: none;

        box-shadow:
            var(--shadow);
    }

    /* =====================================================
    SCROLLBAR
    ===================================================== */

    ::-webkit-scrollbar {

        width: 10px;

        height: 10px;
    }

    ::-webkit-scrollbar-thumb {

        background:
            #cbd5e1;

        border-radius: 20px;
    }

    ::-webkit-scrollbar-thumb:hover {

        background:
            #94a3b8;
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

            padding-top: 3rem;

            max-width: 100%;
        }

        button[data-baseweb="tab"] {

            min-width: 150px;

            font-size: 14px;
        }

        .card {

            padding: 18px;
        }

        .card-title {

            font-size: 20px;
        }
    }

    </style>

    """, unsafe_allow_html=True)
