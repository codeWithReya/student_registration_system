import streamlit as st
import mysql.connector

st.set_page_config(
    page_title="New User Registration",
    page_icon="📝",
    layout="centered"
)

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

st.markdown("""
<style>

.stApp {
    background-color: #06283D;
}

.title {
    background-color: #ad8888;
    color: white;
    text-align: center;
    padding: 18px;
    font-size: 30px;
    font-weight: bold;
    border-radius: 8px;
    margin-bottom: 30px;
}

label {
    font-weight: bold !important;
}

.stTextInput label,
.stSelectbox label {
    color: yellow !important;
}

.registration-box {
    background-color: #ad8888;
    padding: 30px;
    border-radius: 50px;
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
    '<div class="title">New User Registration</div>',
    unsafe_allow_html=True
)
# FORM
with st.form("new_user_form"):
    full_name = st.text_input(
        "Full Name",
        placeholder="Enter Full Name"
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
    role = st.selectbox(
        "Role",
        ["Select Role", "Teacher", "Office Staff", "Admin", "Other Staff"]
    )
    department = st.text_input(
        "Department",
        placeholder="Enter Department"
    )
    register_button = st.form_submit_button(
        "Register",
        use_container_width=True
    )

# REGISTER
if register_button:
    if (
        full_name.strip() == ""
        or user_name.strip() == ""
        or password == ""
        or role == "Select Role"
        or department.strip() == ""
    ):
        st.warning("Please fill all details!")
    else:
        db = None
        cursor = None
        try:
            db = get_database()
            cursor = db.cursor()

            # CHECK USERNAME
            check_query = """
                SELECT *
                FROM login
                WHERE user_name = %s
            """
            cursor.execute(
                check_query,
                (user_name.strip(),)
            )
            result = cursor.fetchone()
            if result:
                st.error("User Name already exists!")
            else:
                # INSERT USER
                query = """
                    INSERT INTO login
                    (
                        full_name,
                        user_name,
                        password,
                        role,
                        department
                    )
                    VALUES (%s, %s, %s, %s, %s)
                """
                values = (
                    full_name.strip(),
                    user_name.strip(),
                    password,
                    role,
                    department.strip()
                )
                cursor.execute(
                    query,
                    values
                )
                db.commit()
                st.success("New User Registered Successfully!")
                st.info("Returning to Login Page...")
                st.switch_page("pages/login_page.py")

        except mysql.connector.Error as e:
            st.error(f"Database Error: {e}")
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

# BACK TO LOGIN
st.write("")
if st.button("Already have an account? Login", use_container_width=True):
    st.switch_page("pages/login_page.py")
