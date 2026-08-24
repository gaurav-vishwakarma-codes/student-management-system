# =====================================================
# History Service
# All direct database operations for the update history
# and deleted history pages (load + restore).
# Pulled out of the routes so routes only handle
# request/response, not raw SQL.
# (Unchanged logic from the Tkinter version — only the
#  import path has moved to app.database.db_connection)
# =====================================================

from app.database.db_connection import (
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
    Returns (restored_count: int, already_active: list, not_found: list).
    - already_active: roll numbers that are already back in `students`
      (e.g. restored earlier, or re-added manually)
    - not_found: roll numbers that no longer exist in deleted_students
      at all (e.g. they were permanently deleted)
    Raises Exception on DB failure (caller should catch it).
    """

    conn   = None
    cursor = None

    restored       = 0
    already_active = []
    not_found      = []

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
                not_found.append(roll_no)
                continue

            # SKIP IF ALREADY ACTIVE
            cursor.execute(
                "SELECT 1 FROM students WHERE roll_no = ?",
                (roll_no,)
            )

            if cursor.fetchone():
                already_active.append(roll_no)
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

        return restored, already_active, not_found

    except Exception:

        if conn:
            conn.rollback()

        raise

    finally:

        close_connection(conn, cursor)


# =====================================================
# PERMANENTLY DELETE STUDENTS
# Removes the given roll numbers from deleted_students
# entirely. Unlike the original soft-delete (students ->
# deleted_students), this is IRREVERSIBLE — there is no
# further table to recover the record from afterwards.
# =====================================================

def permanently_delete_students(roll_nos):
    """
    roll_nos: list of roll numbers to permanently remove
              from deleted_students.
    Returns the number of rows actually deleted.
    Raises Exception on DB failure (caller should catch it).
    """

    conn   = None
    cursor = None

    deleted_count = 0

    try:

        conn, cursor = get_connection()

        for roll_no in roll_nos:

            cursor.execute(
                "DELETE FROM deleted_students WHERE roll_no = ?",
                (roll_no,)
            )

            # cursor.rowcount TELLS US WHETHER A ROW ACTUALLY
            # EXISTED AND WAS REMOVED FOR THIS roll_no
            deleted_count += cursor.rowcount

        conn.commit()

        return deleted_count

    except Exception:

        if conn:
            conn.rollback()

        raise

    finally:

        close_connection(conn, cursor)