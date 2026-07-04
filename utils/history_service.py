# =====================================================
# History Service
# All direct database operations for the update history
# and deleted history windows (load + restore).
# Pulled out of the GUI windows so windows only
# handle UI, not raw SQL.
# =====================================================

from database.db_connection import (
    get_connection,
    close_connection
)


# =====================================================
# GET UPDATED STUDENTS HISTORY
# =====================================================

def get_updated_history():
    """Returns all update-history rows, newest first."""

    conn   = None
    cursor = None

    try:

        conn, cursor = get_connection()

        cursor.execute(
            """
            SELECT update_id, roll_no, old_full_name, old_age,
                   old_gender, old_course, old_email, old_phone,
                   old_address, updated_field, new_value, updated_at
            FROM updated_students
            ORDER BY update_id DESC
            """
        )

        return cursor.fetchall()

    finally:

        close_connection(conn, cursor)


# =====================================================
# GET DELETED STUDENTS HISTORY
# =====================================================

def get_deleted_history():
    """Returns all soft-deleted student rows, newest first."""

    conn   = None
    cursor = None

    try:

        conn, cursor = get_connection()

        cursor.execute(
            """
            SELECT delete_id, roll_no, full_name, age, gender,
                   course, email, phone, address, deleted_at
            FROM deleted_students
            ORDER BY delete_id DESC
            """
        )

        return cursor.fetchall()

    finally:

        close_connection(conn, cursor)


# =====================================================
# RESTORE STUDENTS
# Re-inserts the given roll numbers into students
# and removes them from deleted_students.
# =====================================================

def restore_students(roll_nos):
    """
    roll_nos: list of roll numbers to restore.
    Returns (restored_count: int, skipped_roll_nos: list).
    Raises Exception on DB failure (caller should catch it).
    """

    conn   = None
    cursor = None

    restored = 0
    skipped  = []

    try:

        conn, cursor = get_connection()

        for roll_no in roll_nos:

            # FETCH FULL DATA FROM deleted_students
            cursor.execute(
                "SELECT * FROM deleted_students WHERE roll_no = ?",
                (roll_no,)
            )

            student = cursor.fetchone()

            if student is None:
                skipped.append(roll_no)
                continue

            # SKIP IF ALREADY ACTIVE
            cursor.execute(
                "SELECT 1 FROM students WHERE roll_no = ?",
                (roll_no,)
            )

            if cursor.fetchone():
                skipped.append(roll_no)
                continue

            # RE-INSERT INTO students
            cursor.execute(
                """
                INSERT INTO students (
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

            # REMOVE FROM deleted_students
            cursor.execute(
                "DELETE FROM deleted_students WHERE roll_no = ?",
                (roll_no,)
            )

            restored += 1

        conn.commit()

        return restored, skipped

    except Exception:

        if conn:
            conn.rollback()

        raise

    finally:

        close_connection(conn, cursor)