import sqlite3


def create_tables():
    # ==========================================
    # DATABASE CONNECTION
    # ==========================================

    conn = sqlite3.connect("student.db")

    cursor = conn.cursor()

    # ==========================================
    # ADMIN TABLE
    # ==========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admins(
        admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)


    # ==========================================
    # STUDENTS TABLE
    # ==========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students(

        roll_no INTEGER PRIMARY KEY,

        full_name TEXT NOT NULL,

        age INTEGER CHECK(age > 0) NOT NULL,

        gender TEXT NOT NULL,

        course TEXT NOT NULL,

        email TEXT UNIQUE NOT NULL,

        phone TEXT NOT NULL,

        address TEXT NOT NULL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)


    # ==========================================
    # UPDATED STUDENTS HISTORY TABLE
    # ==========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS updated_students(

        update_id INTEGER PRIMARY KEY AUTOINCREMENT,

        roll_no INTEGER,

        old_full_name TEXT,

        old_age INTEGER,

        old_gender TEXT,

        old_course TEXT,

        old_email TEXT,

        old_phone TEXT,

        old_address TEXT,
        
        updated_field TEXT,
        
        new_value TEXT,

        updated_at DATETIME DEFAULT (
            datetime('now', '+5 hours', '+30 minutes')
        )

    )
    """)


    # ==========================================
    # DELETED STUDENTS HISTORY TABLE
    # ==========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS deleted_students(

        delete_id INTEGER PRIMARY KEY AUTOINCREMENT,

        roll_no INTEGER,

        full_name TEXT,

        age INTEGER,

        gender TEXT,

        course TEXT,

        email TEXT,

        phone TEXT,

        address TEXT,

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

