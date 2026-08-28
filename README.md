# Student Management System

A console-based Student Management System built using Python and SQLite.

This project allows administrators to manage student records with authentication, CRUD operations, history tracking, restore functionality, validations, pagination, and a modular project structure.

---

# Features

* Admin Registration & Login
* Add Student Records
* View Student Records
* Search Students
* Update Student Details
* Delete Student Records
* Restore Deleted Students
* View Updated Students History
* View Deleted Students History
* Track Old Values and New Values During Updates
* SQLite Database Integration
* Input Validation
* Pagination Support
* Modular Project Structure
* Dummy Data Insertion Support

---

# Technologies Used

* Python 3
* SQLite3
* Visual Studio Code (VS Code)

---

# Requirements

* Python 3.10 or higher
* SQLite3 (included with Python)

---

# Project Structure

```text
SMS/
│
├── database/
│   ├── db_connection.py
│   ├── db_creation.py
│   ├── dummy_data.py
│   └── init.py
│
├── operations/
│   ├── add_student.py
│   ├── delete_student.py
│   ├── history.py
│   ├── login.py
│   ├── register_admin.py
│   ├── search_student.py
│   ├── update_student.py
│   ├── view_students.py
│   └── init.py
│
├── utils/
│   ├── db_helper.py
│   ├── display_helper.py
│   ├── input_helper.py
│   ├── messages.py
│   ├── pagination_helper.py
│   ├── password_helper.py
│   ├── update_helper.py
│   ├── validations.py
│   └── init.py
│
├── main.py
├── student.db
├── README.md
└── .gitignore
```

---

# How To Run

## 1. Clone Repository

```bash
git clone <repository-link>
```

## 2. Open Project Folder

```bash
cd SMS
```

## 3. Run Main File

```bash
py main.py
```

This will:

* Create database tables automatically
* Start the Student Management System

---

# Insert Dummy Data

To insert dummy student records:

```bash
py -m database.dummy_data
```

---

# Main Functionalities

## Authentication

* Admin Registration
* Admin Login

## Student Operations

* Add Student
* View Students
* Search Student
* Update Student
* Delete Student

## History Management

* View Updated Student History
* View Deleted Student History
* Restore Deleted Student Records

---

# Database Tables

## admins

Stores administrator account information.

## students

Stores active student records.

## updated_students

Stores update history including:

* Updated Field
* Old Student Data
* New Value
* Update Timestamp

## deleted_students

Stores deleted student records for restoration.

---

# Validation Features

* Roll Number Validation
* Name Validation
* Age Validation
* Gender Validation
* Course Validation
* Email Validation
* Phone Number Validation
* Address Validation
* Duplicate Email Checking
* No-Change Update Detection

---

# Learning Outcomes

This project helped in understanding:

* Python Modular Programming
* SQLite Database Operations
* CRUD Operations
* Input Validation
* Exception Handling
* Database Design
* History Tracking Systems
* Data Restoration Techniques
* Pagination
* Git & GitHub Version Control

---

# Future Improvements

* GUI Version using Tkinter
* Web Version using Flask or Django
* Export Records to Excel/PDF
* Multiple User Roles
* Password Hashing using bcrypt
* Advanced Search Filters
* Student Attendance System
* Dashboard & Analytics

---

# Author

CodeLearner

BCA Student | Python, SQLite & Java Developer | Cybersecurity Enthusiast

---

# License

This project is created for learning and educational purposes.
