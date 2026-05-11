import streamlit as st

# =====================================================
# SAFE CSS IMPORT
# =====================================================

try:

    from styles.style import load_css

    load_css()

except Exception as e:

    st.error(f"CSS ERROR: {e}")

from attendance.attendance_ui import (
    render_attendance_tab
)

from leaves.leaves_ui import (
    render_leaves_tab
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Attendance System",
    layout="wide"
)

# =====================================================
# TABS
# =====================================================

attendance_tab, leave_tab = st.tabs([

    "📊 الحضور والانصراف",

    "🏖️ الإجازات"
])

with attendance_tab:

    render_attendance_tab()

with leave_tab:

    render_leaves_tab()
