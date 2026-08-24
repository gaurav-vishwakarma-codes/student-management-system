# =====================================================
# Database Creation
# Creates all required tables if they don't exist
# (Unchanged logic from the Tkinter version)
# =====================================================

import sqlite3
from app.config import DB_NAME

# =====================================================
# CREATE TABLES
# =====================================================

def create_tables():
    """
    Creates all four tables needed by the application:
    - admins           : stores admin login credentials
    - students         : stores active student records
    - updated_students : stores history of every update made
    - deleted_students : stores soft-deleted student records
    """

    # ==========================================
    # DATABASE CONNECTION
    # ==========================================

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    # ==========================================
    # ADMIN TABLE
    # Stores admin username and hashed password
    # ==========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admins (

        admin_id   INTEGER PRIMARY KEY AUTOINCREMENT,
        username   TEXT UNIQUE NOT NULL,
        password   TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    # ==========================================
    # STUDENTS TABLE
    # Stores active student records
    # roll_no is the PRIMARY KEY (manually entered)
    # email must be unique across all students
    # ==========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (

        roll_no    INTEGER PRIMARY KEY,
        full_name  TEXT NOT NULL,
        age        INTEGER CHECK(age > 0) NOT NULL,
        gender     TEXT NOT NULL,
        course     TEXT NOT NULL,
        email      TEXT UNIQUE NOT NULL,
        phone      TEXT NOT NULL,
        address    TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    # ==========================================
    # UPDATED STUDENTS HISTORY TABLE
    # Records every field update made to a student
    # Stores old values + which field was changed + new value
    # Timestamp uses IST (UTC +5:30)
    # ==========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS updated_students (

        update_id     INTEGER PRIMARY KEY AUTOINCREMENT,
        roll_no       INTEGER,
        old_full_name TEXT,
        old_age       INTEGER,
        old_gender    TEXT,
        old_course    TEXT,
        old_email     TEXT,
        old_phone     TEXT,
        old_address   TEXT,
        updated_field TEXT,
        new_value     TEXT,
        updated_at    DATETIME DEFAULT (
                          datetime('now', '+5 hours', '+30 minutes')
                      )

    )
    """)

    # ==========================================
    # DELETED STUDENTS HISTORY TABLE
    # Records soft-deleted students
    # Students deleted here can be restored later
    # Timestamp uses IST (UTC +5:30)
    # ==========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS deleted_students (

        delete_id  INTEGER PRIMARY KEY AUTOINCREMENT,
        roll_no    INTEGER,
        full_name  TEXT,
        age        INTEGER,
        gender     TEXT,
        course     TEXT,
        email      TEXT,
        phone      TEXT,
        address    TEXT,
        deleted_at DATETIME DEFAULT (
                       datetime('now', '+5 hours', '+30 minutes')
                   )

    )
    """)

    # ==========================================
    # SAVE CHANGES
    # ==========================================

    conn.commit()

    # ==========================================
    # CLOSE CONNECTION
    # ==========================================

    conn.close()