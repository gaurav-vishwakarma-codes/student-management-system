from database.db_connection import (
    get_connection,
    close_connection
)

from utils.messages import (
    error_message
)

from utils.display_helper import display_student

from utils.pagination_helper import paginate_records

from utils.messages import success_message

def view_students():

    conn = None
    cursor = None

    try:

        # DATABASE CONNECTION
        conn, cursor = get_connection()

        # SAFETY CHECK
        if conn is None or cursor is None:
            error_message("Database Connection Failed")
            return
                
        # FETCH ALL STUDENTS
        cursor.execute("""
            SELECT *
            FROM students
            ORDER BY roll_no
        """)
        
        students = cursor.fetchall()

        if not students:
            error_message("No Any Records Found")
            return

        if len(students) > 1:
            success_message(f"Total Records Available: {len(students)}")
                
        # DISPLAY USING PAGINATION
        paginate_records(
            students,
            display_student
        )

    # HANDLE GENERAL ERRORS
    except Exception as error:
        error_message(
            f"Something Went Wrong: {error}"
        )

    # CLOSE CONNECTION
    finally:
        close_connection(conn, cursor)