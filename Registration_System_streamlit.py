import streamlit as st


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Student Registration System",
    page_icon="🎓",
    layout="wide"
)


# =========================================================
# SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_name" not in st.session_state:
    st.session_state.user_name = ""


# =========================================================
# NAVIGATION
# =========================================================

pg = st.navigation([
    st.Page(
        "pages/login_page.py",
        title="Login",
        icon="🔐"
    ),

    st.Page(
        "pages/new_user.py",
        title="New User",
        icon="📝"
    ),

    st.Page(
        "pages/registration_system.py",
        title="Registration System",
        icon="🎓"
    )
])


# =========================================================
# RUN APP
# =========================================================

pg.run()