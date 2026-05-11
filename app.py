import streamlit as st

from styles.style import load_css

from auth.login import require_login

from attendance.attendance_ui import (
    render_attendance_tab
)

from leaves.leaves_ui import (
    render_leaves_tab
)

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(

    page_title="Attendance System",

    layout="wide"
)

# =========================================================
# CSS
# =========================================================

load_css()

# =========================================================
# LOGIN
# =========================================================

require_login(
    "نظام الحضور والانصراف والإجازات"
)

# =========================================================
# MAIN TABS
# =========================================================

attendance_tab, leave_tab = st.tabs([

    "📊 الحضور والانصراف",

    "🏖️ الإجازات"
])

# =========================================================
# ATTENDANCE TAB
# =========================================================

with attendance_tab:

    render_attendance_tab()

# =========================================================
# LEAVES TAB
# =========================================================

with leave_tab:

    render_leaves_tab()
