import streamlit as st
import mysql.connector


def get_database():
    return mysql.connector.connect(
        host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
        port=4000,
        user="5WtwPzksksDPRZX.root",
        password="N5sodO8ZaMzPg4yJ",
        database="student_registration",
        ssl_ca="ca cert.pem",
        ssl_verify_cert=True,
        ssl_verify_identity=True
    )

# PAGE CONFIG
st.set_page_config(
    page_title="Login Page",
    page_icon="🔐",
    layout="centered"
)

st.markdown("""
<style>
.stApp {
    background-color: #06283D;
}

.title {
    background-color: #c36464;
    color: white;
    text-align: center;
    padding: 20px;
    font-size: 32px;
    font-weight: bold;
    border-radius: 5px;
    margin-bottom: 45px;
}


.login-heading {
    color: white;
    text-align: center;
    font-size: 30px;
    font-weight: bold;
    margin-bottom: 20px;
    background-color: #ad8888;
    padding: 20px;
    border-radius: 10px;
}

label {
    color: yellow !important;
    font-weight: bold !important;
}

.stTextInput input {
    font-size: 17px;
}

.stButton button {
    background-color: #f0687c;
    color: white;
    font-size: 17px;
    font-weight: bold;
    border: none;
    border-radius: 5px;
}

.stButton button:hover {
    background-color: #d95368;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# TITLE
st.markdown(
    '<div class="title">Registered Students<br>Login</div>',
    unsafe_allow_html=True
)

# LOGIN BOX
st.markdown(
    '<div class="login-box">',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="login-heading">Admin Login</div>',
    unsafe_allow_html=True
)
user_name = st.text_input(
    "User Name",
    placeholder="Enter User Name"
)
password = st.text_input(
    "Password",
    type="password",
    placeholder="Enter Password"
)
st.markdown("</div>", unsafe_allow_html=True)

# LOGIN BUTTON
st.write("")
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    login_button = st.button("Login", use_container_width=True)

# LOGIN CHECK
if login_button:
    if user_name.strip() == "" or password == "":
        st.warning("Please enter User Name and Password")
    else:
        db = None
        cursor = None
        try:
            db = get_database()
            cursor = db.cursor()
            query = """
                SELECT *
                FROM login
                WHERE user_name = %s
                AND password = %s
            """
            cursor.execute(
                query,
                (user_name.strip(), password)
            )
            result = cursor.fetchone()
            if result:
                st.session_state.logged_in = True
                st.session_state.user_name = user_name.strip()
                st.success("Welcome! Login successful.")
                # Go to Student Registration System
                st.switch_page("pages/registration_system.py")
            else:
                st.error("Invalid User Name or Password")

        except mysql.connector.Error as e:
            st.error(f"Database Error: {e}")
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

# NEW USER
st.write("")
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("New User", use_container_width=True):
        st.switch_page("pages/new_user.py")
