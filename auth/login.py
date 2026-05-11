import streamlit as st

# =========================================================
# USERS
# =========================================================

USERS = {

    "admin": "1234",

    "mohamed": "1234",
}

# =========================================================
# INIT SESSION
# =========================================================

def init_session():

    if "logged_in" not in st.session_state:

        st.session_state["logged_in"] = False

    if "login_user" not in st.session_state:

        st.session_state["login_user"] = ""

    if "refresh_after_login" not in st.session_state:

        st.session_state["refresh_after_login"] = False

# =========================================================
# CHECK USER
# =========================================================

def check_user(username, password):

    username = str(username).strip()

    password = str(password).strip()

    return USERS.get(username) == password

# =========================================================
# LOGIN
# =========================================================

def require_login(title="System"):

    # =====================================================
    # INIT
    # =====================================================

    init_session()

    # =====================================================
    # SAFE REFRESH
    # =====================================================

    if st.session_state.get("refresh_after_login"):

        st.session_state["refresh_after_login"] = False

        st.rerun()

    # =====================================================
    # ALREADY LOGGED
    # =====================================================

    if st.session_state.get("logged_in"):

        with st.sidebar:

            st.success(

                f"👋 {st.session_state.get('login_user')}"
            )

            logout_btn = st.button(

                "🚪 تسجيل الخروج",

                use_container_width=True
            )

            if logout_btn:

                st.session_state["logged_in"] = False

                st.session_state["login_user"] = ""

                st.rerun()

        return

    # =====================================================
    # LOGIN SCREEN
    # =====================================================

    st.markdown(
        f"""
        <div style="
            text-align:center;
            padding:20px;
            font-size:28px;
            font-weight:bold;
            color:white;
        ">
        {title}
        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns([1,2,1])

    with c2:

        with st.container(border=True):

            st.markdown(
                "### 🔐 تسجيل الدخول"
            )

            username = st.text_input(
                "اسم المستخدم"
            )

            password = st.text_input(
                "كلمة المرور",
                type="password"
            )

            login_btn = st.button(

                "دخول",

                use_container_width=True
            )

            if login_btn:

                valid = check_user(
                    username,
                    password
                )

                if valid:

                    st.session_state["logged_in"] = True

                    st.session_state["login_user"] = username

                    st.session_state["refresh_after_login"] = True

                    st.success(
                        "تم تسجيل الدخول بنجاح"
                    )

                    st.stop()

                else:

                    st.error(
                        "اسم المستخدم أو كلمة المرور غير صحيحة"
                    )

    st.stop()
