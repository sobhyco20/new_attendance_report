import streamlit as st

def load_css():

    st.markdown(
        """
        <style>

        html, body, .stApp {
            direction: rtl;
            text-align: right;
            font-family: "Segoe UI", Tahoma, sans-serif;
        }

        .stApp {
            background: linear-gradient(180deg, #020617 0%, #071226 100%);
            color: #f8fafc;
        }

        .block-container {
            padding-top: 1rem;
            padding-bottom: 2rem;
            max-width: 100%;
        }

        #MainMenu, footer, header {
            visibility: hidden;
        }

        .summary-header {
            background: linear-gradient(90deg, #111827, #0f172a);
            padding: 30px;
            border-radius: 24px;
            margin-bottom: 25px;
            border: 1px solid rgba(255,255,255,0.08);
            box-shadow: 0 10px 30px rgba(0,0,0,0.25);
        }

        .summary-title {
            color: white;
            font-size: 38px;
            font-weight: 900;
            margin-bottom: 10px;
        }

        .summary-subtitle {
            color: #cbd5e1;
            font-size: 18px;
        }

        .employee-box {
            background: linear-gradient(145deg, #111827, #0f172a);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 22px;
            padding: 24px;
            box-shadow: 0 0 20px rgba(0,0,0,0.30);
            min-height: 120px;
            margin-bottom: 15px;
        }

        .employee-box-inner {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 15px;
        }

        .employee-icon {
            font-size: 26px;
            width: 60px;
            height: 60px;
            border-radius: 16px;
            background: rgba(255,255,255,0.06);
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .employee-label {
            color: #cbd5e1;
            font-size: 17px;
            margin-bottom: 8px;
        }

        .employee-value {
            color: white;
            font-size: 28px;
            font-weight: 800;
        }

        .kpi-card {
            background: linear-gradient(145deg, #111827, #0f172a);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 22px;
            padding: 26px;
            min-height: 210px;
            box-shadow: 0 0 25px rgba(0,0,0,0.35);
            margin-bottom: 18px;
        }

        .kpi-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 18px;
        }

        .kpi-icon {
            font-size: 28px;
            width: 68px;
            height: 68px;
            border-radius: 18px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .kpi-title {
            color: white;
            font-size: 24px;
            font-weight: 800;
        }

        .kpi-value {
            font-size: 48px;
            font-weight: 900;
            line-height: 1.2;
            margin-top: 10px;
        }

        .kpi-subtitle {
            color: #cbd5e1;
            font-size: 18px;
            margin-top: 12px;
        }

        .blue { color: #60a5fa; }
        .green { color: #4ade80; }
        .red { color: #f87171; }
        .purple { color: #c084fc; }
        .orange { color: #fb923c; }
        .pink { color: #f472b6; }

        .bg-blue { background: rgba(96,165,250,0.18); }
        .bg-green { background: rgba(74,222,128,0.18); }
        .bg-red { background: rgba(248,113,113,0.18); }
        .bg-purple { background: rgba(192,132,252,0.18); }
        .bg-orange { background: rgba(251,146,60,0.18); }
        .bg-pink { background: rgba(244,114,182,0.18); }

        .export-box {
            background: linear-gradient(90deg, #111827, #0f172a);
            padding: 24px;
            border-radius: 24px;
            border: 1px solid rgba(255,255,255,0.08);
            margin-top: 25px;
            margin-bottom: 20px;
        }

        .export-title {
            color: white;
            font-size: 28px;
            font-weight: 800;
        }

        .stButton button,
        .stDownloadButton button {
            width: 100%;
            border-radius: 14px;
            border: none;
            padding: 12px 18px;
            font-weight: bold;
            color: white;
            background: linear-gradient(135deg, #2563eb, #4338ca);
        }

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

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f172a, #111c30);
        }

        </style>
        """,
        unsafe_allow_html=True
    )