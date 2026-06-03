from database.db_connection import (
    get_connection,
    close_connection
)

from utils.db_helper import is_table_empty

from utils.input_helper import get_valid_input
from utils.validations import validate_roll_no


from utils.messages import (
    success_message,
    error_message
)

from utils.history_display_helper import (
    display_updated_history,
    display_deleted_history
)

from utils.pagination_helper import paginate_records


# VIEW UPDATED HISTORY
def view_updated_history():

    conn = None
    cursor = None

    try:

        # DATABASE CONNECTION
        conn, cursor = get_connection()

        # SAFETY CHECK
        if conn is None or cursor is None:
            error_message("Database Connection Failed")
            return
        
        # CHECK table empty or not before user query
        if is_table_empty(cursor, "updated_students"):
            error_message(
                "No Updated History Found"
            )
            return

        # FETCH UPDATED HISTORY
        cursor.execute("""
            SELECT *
            FROM updated_students
            ORDER BY updated_at DESC
        """)

        records = cursor.fetchall()

        # IF ONLY ONE STUDENT EXISTS
        if len(records) == 1:
            paginate_records(
                records,
                display_updated_history
            )
        else:
            success_message(f"Total Updated History Available: {len(records)}")

            # DISPLAY RECORDS WITH PAGINATION
            paginate_records(
                records,
                display_updated_history
            )

    # HANDLE GENERAL ERRORS
    except Exception as error:
        error_message(f"Something Went Wrong: {error}")

    # CLOSE CONNECTION
    finally:
        close_connection(conn, cursor)


# VIEW DELETED HISTORY
def view_deleted_history():

    conn = None
    cursor = None

    try:

        # DATABASE CONNECTION
        conn, cursor = get_connection()

        # SAFETY CHECK
        if conn is None or cursor is None:
            error_message("Database Connection Failed")
            return
        
        # CHECK table empty or not before user query
        if is_table_empty(cursor, "deleted_students"):
            error_message(
                "No Deleted History Found"
            )
            return

        # FETCH DELETED HISTORY
        cursor.execute("""
            SELECT *
            FROM deleted_students
            ORDER BY deleted_at DESC
        """)

        records = cursor.fetchall()

        # IF ONLY ONE STUDENT EXISTS
        if len(records) == 1:
            paginate_records(
                records,
                display_deleted_history
            )
        else:
            success_message(f"Total Deleted History Available: {len(records)}")

            # DISPLAY RECORDS WITH PAGINATION
            paginate_records(
                records,
                display_deleted_history
            )

    # HANDLE GENERAL ERRORS
    except Exception as error:
        error_message(f"Something Went Wrong: {error}")

    # CLOSE CONNECTION
    finally:
        close_connection(conn, cursor)


# RESTORE DELETED STUDENT
def restore_deleted_student():

    conn = None
    cursor = None

    try:
        # DATABASE CONNECTION
        conn, cursor = get_connection()

        # SAFETY CHECK
        if conn is None or cursor is None:
            error_message("Database Connection Failed")
            return
        
        # CHECK table empty or not before user query
        if is_table_empty(cursor, "deleted_students"):
            error_message(
                "No Deleted History Found"
            )
            return

        # FETCH DELETED RECORDS
        cursor.execute("""
            SELECT *
            FROM deleted_students
            ORDER BY deleted_at DESC
        """)

        deleted_records = cursor.fetchall()

        # CASE 1: SINGLE RECORD
        if len(deleted_records) == 1:

            student = deleted_records[0]

            paginate_records(
                deleted_records,
                display_deleted_history
            )

            confirm = input(
                "\nOnly One Deleted Record Found. Restore it? (y/n): "
            ).strip().lower()

            if confirm != "y":
                error_message("Restore Operation Cancelled")
                return

            roll_no = student["roll_no"]

        # CASE 2: MULTIPLE RECORDS
        else:
            success_message(f"Total Deleted History Available: {len(deleted_records)}")

            paginate_records(
                deleted_records,
                display_deleted_history
            )

            # INPUT ROLL NUMBER
            roll_no = int(
                get_valid_input(
                    "\nEnter Roll Number To Restore: ",
                    validate_roll_no
                )
            )

            # FETCH STUDENT FROM deleted_students
            cursor.execute("""
                SELECT *
                FROM deleted_students
                WHERE roll_no=?
            """, (roll_no,))

            student = cursor.fetchone()

            # CHECK STUDENT EXISTS
            if student is None:
                error_message(
                    "Student Not Found In Deleted History"
                )
                return
            
            confirm = input(
                "\nAre You Sure You Want To Restore This Student? (y/n): "
            ).strip().lower()

            if confirm != "y":
                error_message("Restore Operation Cancelled")
                return

        # CHECK IF EXISTS IN MAIN TABLE
        cursor.execute("""
            SELECT 1
            FROM students
            WHERE roll_no=?
        """, (roll_no,))

        if cursor.fetchone():
            error_message(
                "Student Already Exists In Main Table"
            )
            return

        # RESTORE STUDENT
        cursor.execute("""
        INSERT INTO students(

            roll_no,
            full_name,
            age,
            gender,
            course,
            email,
            phone,
            address

        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (

            student["roll_no"],
            student["full_name"],
            student["age"],
            student["gender"],
            student["course"],
            student["email"],
            student["phone"],
            student["address"]

        ))

        # REMOVE FROM deleted_students
        cursor.execute("""
            DELETE FROM deleted_students
            WHERE roll_no=?
        """, (roll_no,))

        # SAVE CHANGES
        conn.commit()

        # SUCCESS MESSAGE
        success_message(
            "Student Restored Successfully"
        )

    # HANDLE GENERAL ERRORS
    except Exception as error:
        if conn:
            conn.rollback()
        error_message(f"Something Went Wrong: {error}")

    # CLOSE CONNECTION
    finally:
        close_connection(conn, cursor)