# =====================================================
# Student Service
# All direct database operations for student records
# (add / view / search / delete / delete all).
# =====================================================

from database.db_connection import (
    get_connection,
    close_connection
)


# =====================================================
# ADD STUDENT
# =====================================================

def add_student(student):
    """
    Inserts a new student record.
    student: dict with keys roll_no, full_name, age, gender,
             course, email, phone, address
    Returns (success: bool, message: str)
    """

    conn   = None
    cursor = None

    try:

        conn, cursor = get_connection()

        # CHECK FOR DUPLICATE ROLL NUMBER
        cursor.execute(
            "SELECT 1 FROM students WHERE roll_no = ?",
            (student["roll_no"],)
        )

        if cursor.fetchone():
            return False, "Roll Number Already Exists"

        # CHECK FOR DUPLICATE EMAIL
        cursor.execute(
            "SELECT 1 FROM students WHERE email = ?",
            (student["email"],)
        )

        if cursor.fetchone():
            return False, "Email Already Exists"

        # INSERT THE NEW STUDENT
        cursor.execute(
            """
            INSERT INTO students (
                roll_no, full_name, age, gender,
                course, email, phone, address
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                student["roll_no"], student["full_name"], student["age"],
                student["gender"],  student["course"],    student["email"],
                student["phone"],   student["address"]
            )
        )

        conn.commit()

        return True, "Student Added Successfully"

    except Exception as error:

        if conn:
            conn.rollback()

        return False, str(error)

    finally:

        close_connection(conn, cursor)


# =====================================================
# GET STUDENT BY ROLL NUMBER
# =====================================================

def get_student_by_roll(roll_no):
    """Returns the student row for the given roll number, or None."""

    conn   = None
    cursor = None

    try:

        conn, cursor = get_connection()

        cursor.execute(
            """
            SELECT roll_no, full_name, age, gender,
                   course, email, phone, address
            FROM students
            WHERE roll_no = ?
            """,
            (roll_no,)
        )

        return cursor.fetchone()

    finally:

        close_connection(conn, cursor)


# =====================================================
# GET ALL STUDENTS
# =====================================================

def get_all_students():
    """Returns all active students ordered by roll number."""

    conn   = None
    cursor = None

    try:

        conn, cursor = get_connection()

        cursor.execute(
            """
            SELECT roll_no, full_name, age, gender,
                   course, email, phone, address
            FROM students
            ORDER BY roll_no
            """
        )

        return cursor.fetchall()

    finally:

        close_connection(conn, cursor)


# =====================================================
# COUNT STUDENTS
# Used to enable/disable the "Delete All" button
# =====================================================

def count_students():

    conn   = None
    cursor = None

    try:

        conn, cursor = get_connection()

        cursor.execute("SELECT COUNT(*) FROM students")

        return cursor.fetchone()[0]

    finally:

        close_connection(conn, cursor)


# =====================================================
# DELETE STUDENT (SOFT DELETE)
# Moves the record to deleted_students before removing it
# =====================================================

def delete_student(roll_no):
    """Returns (success: bool, message: str)."""

    conn   = None
    cursor = None

    try:

        conn, cursor = get_connection()

        # FETCH FULL STUDENT DATA BEFORE DELETING
        cursor.execute(
            """
            SELECT roll_no, full_name, age, gender,
                   course, email, phone, address
            FROM students
            WHERE roll_no = ?
            """,
            (roll_no,)
        )

        student = cursor.fetchone()

        if student is None:
            return False, "No student found to delete"

        # STEP 1 — SAVE TO deleted_students
        cursor.execute(
            """
            INSERT INTO deleted_students (
                roll_no, full_name, age, gender,
                course, email, phone, address
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                student["roll_no"],  student["full_name"],
                student["age"],      student["gender"],
                student["course"],   student["email"],
                student["phone"],    student["address"]
            )
        )

        # STEP 2 — REMOVE FROM students
        cursor.execute(
            "DELETE FROM students WHERE roll_no = ?",
            (roll_no,)
        )

        conn.commit()

        return True, "Student Deleted Successfully"

    except Exception as error:

        if conn:
            conn.rollback()

        return False, str(error)

    finally:

        close_connection(conn, cursor)


# =====================================================
# DELETE ALL STUDENTS (SOFT DELETE)
# =====================================================

def delete_all_students():
    """Returns (success: bool, message: str, deleted_count: int)."""

    conn   = None
    cursor = None

    try:

        conn, cursor = get_connection()

        cursor.execute(
            """
            SELECT roll_no, full_name, age, gender,
                   course, email, phone, address
            FROM students
            """
        )

        students = cursor.fetchall()

        if not students:
            return False, "No students found to delete.", 0

        # STEP 1 — INSERT ALL INTO deleted_students
        cursor.executemany(
            """
            INSERT INTO deleted_students (
                roll_no, full_name, age, gender,
                course, email, phone, address
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    s["roll_no"], s["full_name"], s["age"],
                    s["gender"],  s["course"],     s["email"],
                    s["phone"],   s["address"]
                )
                for s in students
            ]
        )

        # STEP 2 — DELETE ALL FROM students
        cursor.execute("DELETE FROM students")

        conn.commit()

        count = len(students)

        return True, f"All {count} student(s) deleted successfully.", count

    except Exception as error:

        if conn:
            conn.rollback()

        return False, str(error), 0

    finally:

        close_connection(conn, cursor)