# =====================================================
# Student Service
# All direct database operations for student records
# (add / view / search / delete / delete all).
# (Unchanged logic from the Tkinter version — only the
#  import path has moved to app.database.db_connection)
# =====================================================

from app.database.db_connection import (
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
# SEARCH STUDENTS (FLEXIBLE — MULTIPLE FIELDS)
# Powers the "Search Student" page, letting the user
# search by roll number, full name, course, email,
# phone, or address instead of only roll number.
# =====================================================

# ONLY THESE FIELDS ARE SEARCHABLE — used to safely build
# the WHERE clause, since we never insert raw user input
# into the SQL string itself (only into ? placeholders).
SEARCHABLE_FIELDS = {
    "roll_no":   "roll_no = ?",         # EXACT MATCH (it's a number)
    "age":       "age = ?",             # EXACT MATCH (it's a number)
    "full_name": "full_name LIKE ?",    # PARTIAL, CASE-INSENSITIVE MATCH ("CONTAINS")
    "gender":    "gender LIKE ?",       # "STARTS WITH" MATCH — SEE NOTE BELOW
    "course":    "course LIKE ?",
    "email":     "email LIKE ?",
    "phone":     "phone LIKE ?",
    "address":   "address LIKE ?",
}

# FIELDS THAT NEED AN EXACT NUMERIC MATCH RATHER THAN A
# "CONTAINS" TEXT MATCH
_EXACT_MATCH_FIELDS = {"roll_no", "age"}

# GENDER NEEDS "STARTS WITH" RATHER THAN "CONTAINS ANYWHERE":
# the word "Male" is literally a substring of "Female" (Fe-MALE),
# so a plain %Male% search would wrongly return Female students
# too. Matching from the start of the value avoids that overlap
# while still allowing partial typing, e.g. "Mal" or "Fem".
_PREFIX_MATCH_FIELDS = {"gender"}


def search_students(field, value):
    """
    Searches active students by the given field.
    - "roll_no" / "age": exact numeric match (value must already
      be a valid int-string)
    - "gender": case-insensitive "starts with" match (e.g. "Mal"
      matches "Male" but NOT "Female" — see note above)
    - all other fields: case-insensitive partial "contains" match
      (e.g. "sha" matches "Rahul Sharma")
    Returns a list of matching rows (possibly empty).
    Raises ValueError if `field` isn't a recognised searchable field.
    """

    if field not in SEARCHABLE_FIELDS:
        raise ValueError(f"'{field}' is not a searchable field.")

    conn   = None
    cursor = None

    try:

        conn, cursor = get_connection()

        condition = SEARCHABLE_FIELDS[field]

        if field in _EXACT_MATCH_FIELDS:
            params = (int(value),)
        elif field in _PREFIX_MATCH_FIELDS:
            params = (f"{value}%",)   # STARTS WITH — NO LEADING %
        else:
            params = (f"%{value}%",)  # CONTAINS ANYWHERE

        cursor.execute(
            f"""
            SELECT roll_no, full_name, age, gender,
                   course, email, phone, address
            FROM students
            WHERE {condition}
            ORDER BY roll_no
            """,
            params
        )

        return cursor.fetchall()

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


# =====================================================
# BULK DELETE STUDENTS (SOFT DELETE, SPECIFIC LIST)
# Deletes a specific set of students in one go — e.g.
# every student found by a "search by criteria" result
# (all MCom students, everyone aged 20, etc.), not the
# single-student delete and not delete-EVERYTHING.
# Same soft-delete behaviour as delete_student(): each
# record is preserved in deleted_students and can still
# be restored or permanently removed from there.
# =====================================================

def bulk_delete_students(roll_nos):
    """
    roll_nos: list of roll numbers to soft-delete.
    Returns (success: bool, message: str, deleted_count: int)
    """

    conn   = None
    cursor = None

    try:

        conn, cursor = get_connection()

        deleted_count = 0

        for roll_no in roll_nos:

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
                # ALREADY GONE (e.g. deleted by someone else
                # since the search results were shown) — skip
                continue

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

            cursor.execute(
                "DELETE FROM students WHERE roll_no = ?",
                (roll_no,)
            )

            deleted_count += 1

        conn.commit()

        if deleted_count == 0:
            return False, "No matching students found to delete.", 0

        return True, f"{deleted_count} student(s) deleted successfully.", deleted_count

    except Exception as error:

        if conn:
            conn.rollback()

        return False, str(error), 0

    finally:

        close_connection(conn, cursor)