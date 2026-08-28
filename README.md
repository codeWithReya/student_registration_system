# 🎓 Student Registration System

A web-based **Student Registration System** developed using **Python, Streamlit, MySQL and TiDB Cloud**.

This application provides a simple and user-friendly interface for staff to manage student registration records, search existing students, register new students, and manage student information.

---

## 🚀 Live Demo

👉 **[Open Student Registration System](https://studentregistrationsystem-bncj5u8yucwvmasfsmpkw8.streamlit.app)**

> The live application is deployed using Streamlit Cloud.

---

## 📌 Features

### 🔐 Login System
- Secure staff login
- New user registration
- Username and password authentication
- Role and department information

### 📝 Student Registration
- Automatically generated registration number
- Student full name
- Date of birth
- Gender
- Class
- Religion
- Address

### 👨‍👩‍👧 Parent Details
- Father's name
- Father's occupation
- Father's qualification
- Mother's name
- Mother's occupation
- Mother's qualification

### 🔎 Search Student
- Search students using registration number
- Fetch student information from the database
- Display saved student details
- Display previously uploaded student photo

### 📷 Student Photo
- Upload student photo
- Supports JPG, JPEG and PNG
- Automatically generates a unique filename
- Displays uploaded student photo

### 🔄 Form Controls
- Save student registration
- Reset registration form
- Logout
- Exit back to login

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| 🐍 Python | Application programming |
| 🎈 Streamlit | Web application interface |
| 🗄️ MySQL | Database |
| ☁️ TiDB Cloud | Cloud database hosting |
| 🔗 mysql-connector-python | Python-MySQL connection |
| 🎨 HTML/CSS | UI customization |
| 🆔 UUID | Unique photo filenames |

---

## 📂 Project Structure

```text
Student-Registration-System/
│
├── Registration_System_streamlit.py
│
├── pages/
│   ├── login_page.py
│   ├── new_user.py
│   └── registration_system.py
│
├── student_photos/
│
├── icon.png
├── searchBox.jpg
├── searchIcon.jpg
│
├── requirements.txt
└── README.md
