import streamlit as st
import mysql.connector
from datetime import date, datetime
import os
import uuid

st.set_page_config(
    page_title="Student Registration System",
    page_icon="🎓",
    layout="wide"
)

# LOGIN CHECK
if not st.session_state.get("logged_in", False):
    st.warning("Please login first.")
    if st.button("Go to Login"):
        st.switch_page("pages/login_page.py")
    st.stop()

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

# NEXT REGISTRATION NUMBER
def get_next_registration_no():
    db = None
    cursor = None
    try:
        db = get_database()
        cursor = db.cursor()
        cursor.execute("""
            SELECT MAX(CAST(registration_no AS UNSIGNED))
            FROM students
        """)
        result = cursor.fetchone()
        if result[0] is None:
            return "2026000001"
        return str(int(result[0]) + 1)
    except mysql.connector.Error as e:
        st.error(f"Database Error: {e}")
        return "2026000001"
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

# SESSION STATE
if "form_version" not in st.session_state:
    st.session_state.form_version = 0

if "search_result" not in st.session_state:
    st.session_state.search_result = None

if "registration_no" not in st.session_state:
    st.session_state.registration_no = (
        get_next_registration_no()
    )

st.markdown("""
<style>
.stApp {
    background-color: #06283D;
}

.top-bar {
    background-color: #f0687c;
    color: white;
    padding: 10px;
    text-align: center;
    font-size: 15px;
    font-weight: bold;
}

.title {
    background-color: #c36464;
    color: white;
    text-align: center;
    padding: 18px;
    font-size: 30px;
    font-weight: bold;
}

.section {
    background-color: #EDEDED;
    color: #06283D;
    padding: 10px;
    border-radius: 5px;
    font-size: 21px;
    font-weight: bold;
    margin-top: 20px;
    margin-bottom: 15px;
}

label {
    font-weight: bold !important;
}

.stTextInput label,
.stDateInput label,
.stRadio label,
.stSelectbox label,
.stFileUploader label {
    color: white !important;
}

.stButton button {
    font-weight: bold;
    border-radius: 5px;
}
</style>
""", unsafe_allow_html=True)

# TOP BAR
st.markdown("""
<div class="top-bar">
Email: studentregistration4521@gmail.com
&nbsp;&nbsp; | &nbsp;&nbsp;
Mobile: 9876543210
&nbsp;&nbsp; | &nbsp;&nbsp;
2026-2027 Student Registrations Open
</div>
""", unsafe_allow_html=True)

# TITLE
st.markdown(
    '<div class="title">STUDENT REGISTRATION SYSTEM</div>',
    unsafe_allow_html=True
)

# LOGOUT
col1, col2 = st.columns([8, 1])
with col1:
    st.write(f"Logged in as: **{st.session_state.get('user_name', '')}**")

with col2:
    if st.button("Logout"):
        st.session_state.clear()
        st.switch_page("pages/login_page.py")

# SEARCH
st.markdown(
    '<div class="section">Search Student</div>',
    unsafe_allow_html=True
)

search_col1, search_col2 = st.columns([5, 1])
with search_col1:
    search_registration = st.text_input(
        "Registration Number",
        placeholder="Enter registration number",
        key=f"search_{st.session_state.form_version}"
    )

with search_col2:
    st.write("")
    search_button = st.button(
        "🔍 Search",
        use_container_width=True
    )

# SEARCH DATA
if search_button:
    if search_registration.strip() == "":
        st.error("Please enter registration number")

    else:
        db = None
        cursor = None
        try:
            db = get_database()
            cursor = db.cursor()
            query = """
                SELECT
                    registration_no,
                    full_name,
                    dob,
                    gender,
                    class,
                    religion,
                    address,
                    father_name,
                    father_occupation,
                    father_qualification,
                    mother_name,
                    mother_occupation,
                    mother_qualification,
                    photo
                FROM students
                WHERE registration_no = %s
            """
            cursor.execute(
                query,
                (search_registration.strip(),)
            )
            result = cursor.fetchone()
            if result is None:
                st.session_state.search_result = None
                st.error("No student found with this registration number!")
            else:
                # Save complete database result
                st.session_state.search_result = result
                # Create new widget keys
                st.session_state.form_version += 1
                st.success("Student details found successfully!")
                # Refresh page so all fields get database values
                st.rerun()
        except mysql.connector.Error as e:
            st.error(f"Database Error: {e}")
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

# GET SEARCH RESULT
data = st.session_state.search_result

# STUDENT DETAILS
st.markdown(
    '<div class="section">Student Details</div>',
    unsafe_allow_html=True
)
student_col1, student_col2 = st.columns(2)

# FIRST COLUMN
with student_col1:
    # REGISTRATION NUMBER
    if data:
        reg_value = str(data[0])
    else:
        reg_value = st.session_state.registration_no
    registration_no = st.text_input(
        "Registration No.",
        value=reg_value,
        disabled=True,
        key=f"registration_{st.session_state.form_version}"
    )

    # FULL NAME
    full_name = st.text_input(
        "Full Name",
        value=(
            str(data[1])
            if data and data[1]
            else ""
        ),
        key=f"name_{st.session_state.form_version}"
    )

    # DATE OF BIRTH
    dob_value = date.today()
    if data and data[2]:
        try:
            if isinstance(data[2], datetime):
                dob_value = data[2].date()
            elif isinstance(data[2], date):
                dob_value = data[2]
            else:
                dob_text = str(data[2]).strip()
    
                date_formats = [
                    "%Y-%m-%d",
                    "%Y-%m-%d %H:%M:%S",
                    "%d/%m/%Y",
                    "%d-%m-%Y",
                    "%Y/%m/%d",
                    "%m/%d/%Y"
                ]
    
                for fmt in date_formats:
                    try:
                        dob_value = datetime.strptime(
                            dob_text,
                            fmt
                        ).date()
                        break
                    except ValueError:
                        continue
    
        except Exception:
            dob_value = date.today()
    dob = st.date_input(
        "Date of Birth",
        value=dob_value,
        min_value=date(1950, 1, 1),
        max_value=date.today(),
        key=f"dob_{st.session_state.form_version}"
    )

    # GENDER
    gender_value = (
        str(data[3])
        if data and data[3]
        else "Male"
    )
    gender = st.radio(
        "Gender",
        ["Male", "Female"],
        index=(
            0
            if gender_value == "Male"
            else 1
        ),
        horizontal=True,
        key=f"gender_{st.session_state.form_version}"
    )

# SECOND COLUMN
with student_col2:

    classes = [
        "Select Class",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "11",
        "12"
    ]

    # CLASS
    if data and data[4]:
        class_value = str(data[4])
    else:
        class_value = "Select Class"
    if class_value not in classes:
        class_value = "Select Class"
    student_class = st.selectbox(
        "Class",
        classes,
        index=classes.index(class_value),
        key=f"class_{st.session_state.form_version}"
    )

    # RELIGION
    religion = st.text_input(
        "Religion",
        value=(
            str(data[5])
            if data and data[5]
            else ""
        ),
        key=f"religion_{st.session_state.form_version}"
    )

    # ADDRESS
    address = st.text_input(
        "Address",
        value=(
            str(data[6])
            if data and data[6]
            else ""
        ),
        key=f"address_{st.session_state.form_version}"
    )

    # REGISTRATION DATE
    registration_date = st.text_input(
        "Date",
        value=date.today().strftime("%d/%m/%Y"),
        disabled=True,
        key=f"date_{st.session_state.form_version}"
    )

# PARENT DETAILS
st.markdown(
    '<div class="section">Parent\'s Details</div>',
    unsafe_allow_html=True
)
parent_col1, parent_col2 = st.columns(2)

# FATHER DETAILS
with parent_col1:
    father_name = st.text_input(
        "Father's Name",
        value=(
            str(data[7])
            if data and data[7]
            else ""
        ),
        key=f"father_{st.session_state.form_version}"
    )
    father_occupation = st.text_input(
        "Father's Occupation",
        value=(
            str(data[8])
            if data and data[8]
            else ""
        ),
        key=f"father_occ_{st.session_state.form_version}"
    )
    father_qualification = st.text_input(
        "Father's Qualification",
        value=(
            str(data[9])
            if data and data[9]
            else ""
        ),
        key=f"father_qual_{st.session_state.form_version}"
    )

# MOTHER DETAILS
with parent_col2:
    mother_name = st.text_input(
        "Mother's Name",
        value=(
            str(data[10])
            if data and data[10]
            else ""
        ),
        key=f"mother_{st.session_state.form_version}"
    )
    mother_occupation = st.text_input(
        "Mother's Occupation",
        value=(
            str(data[11])
            if data and data[11]
            else ""
        ),
        key=f"mother_occ_{st.session_state.form_version}"
    )
    mother_qualification = st.text_input(
        "Mother's Qualification",
        value=(
            str(data[12])
            if data and data[12]
            else ""
        ),
        key=f"mother_qual_{st.session_state.form_version}"
    )

# PHOTO
st.markdown(
    '<div class="section">Student Photo</div>',
    unsafe_allow_html=True
)
photo_col1, photo_col2 = st.columns(2)

# UPLOAD PHOTO
with photo_col1:
    uploaded_photo = st.file_uploader(
        "Upload Student Photo",
        type=["jpg", "jpeg", "png"],
        key=f"photo_{st.session_state.form_version}"
    )

# SHOW PHOTO
with photo_col2:
    if uploaded_photo:
        st.image(
            uploaded_photo,
            width=290
        )

    elif data and data[13]:
        old_photo = str(data[13])
        if os.path.exists(old_photo):
            st.image(
                old_photo,
                width=290
            )
        else:
            st.warning("Photo file was not found.")
    else:
        st.info("No photo selected.")

# BUTTONS
st.write("")
button1, button2, button3 = st.columns(3)

# SAVE
with button1:
    save_button = st.button(
        "💾 Save",
        use_container_width=True
    )

if save_button:
    if full_name.strip() == "":
        st.error("Please enter student's full name")

    elif student_class == "Select Class":
        st.error("Please select class")

    else:
        photo_path = ""
        if uploaded_photo:
            folder = "student_photos"
            os.makedirs(
                folder,
                exist_ok=True
            )

            extension = os.path.splitext(
                uploaded_photo.name
            )[1]

            unique_name = (
                str(uuid.uuid4()) + extension
            )

            photo_path = os.path.join(
                folder,
                unique_name
            )

            with open(
                photo_path,
                "wb"
            ) as file:
                file.write(
                    uploaded_photo.getbuffer()
                )

        db = None
        cursor = None
        try:
            db = get_database()
            cursor = db.cursor()
            sql = """
                INSERT INTO students
                (
                    registration_no,
                    full_name,
                    dob,
                    gender,
                    class,
                    religion,
                    address,
                    father_name,
                    father_occupation,
                    father_qualification,
                    mother_name,
                    mother_occupation,
                    mother_qualification,
                    photo
                )
                VALUES
                (
                    %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s
                )
            """
            values = (
                registration_no,
                full_name.strip(),
                dob,
                gender,
                student_class,
                religion.strip(),
                address.strip(),
                father_name.strip(),
                father_occupation.strip(),
                father_qualification.strip(),
                mother_name.strip(),
                mother_occupation.strip(),
                mother_qualification.strip(),
                photo_path
            )
            cursor.execute(
                sql,
                values
            )

            db.commit()
            st.success("Student Registration Saved Successfully!")

            # New registration number
            st.session_state.registration_no = (
                get_next_registration_no()
            )

            # Clear searched data
            st.session_state.search_result = None

            # Create fresh widgets
            st.session_state.form_version += 1
            st.rerun()
        except mysql.connector.IntegrityError:
            st.error("This Registration Number already exists!")
        except mysql.connector.Error as e:
            st.error(f"Database Error: {e}")
        except Exception as e:
            st.error(f"Error: {e}")
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

# RESET
with button2:
    reset_button = st.button(
        "🔄 Reset",
        use_container_width=True
    )

if reset_button:
    st.session_state.search_result = None
    st.session_state.registration_no = (
        get_next_registration_no()
    )
    st.session_state.form_version += 1
    st.rerun()

# EXIT
with button3:
    exit_button = st.button(
        "🚪 Exit",
        use_container_width=True
    )

if exit_button:
    st.session_state.clear()
    st.switch_page("pages/login_page.py")
