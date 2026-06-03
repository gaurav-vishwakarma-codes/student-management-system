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

from utils.display_helper import display_student

from utils.pagination_helper import paginate_records

def delete_student():

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
        if is_table_empty(cursor, "students"):
            error_message(
                "No Students Available"
            )
            return

        # CHECK TOTAL STUDENTS
        cursor.execute("""
            SELECT *
            FROM students
        """)

        total_students = cursor.fetchall()

        # IF ONLY ONE STUDENT EXISTS
        if len(total_students ) == 1:
            paginate_records(
                        total_students,
                        display_student
                    )
            roll_no = total_students[0]["roll_no"]
        else:

            print(f"\nTotal Students Available: {len(total_students)}")
        
            # INPUT ROLL NUMBER
            roll_no = int(
                get_valid_input(
                    "\nEnter Roll Number To Delete: ",
                    validate_roll_no
                )
            )

        # FETCH specific STUDENT DATA
        cursor.execute("""
            SELECT *
            FROM students
            WHERE roll_no=?
        """, (roll_no,))

        student = cursor.fetchone()

        # check specific student exists
        if student is None:
            error_message("Student Not Found")
            return
        
        # DISPLAY STUDENT BEFORE DELETE
        display_student(student)

        # CONFIRM DELETE
        confirm = input(
            f"\nDelete Roll No {student['roll_no']} ({student['full_name']}) ? (y/n): "
        ).lower().strip()

        if confirm != "y":
            error_message(
                "Delete Operation Cancelled"
            )
            return

        # STORE DELETED DATA
        cursor.execute("""
        INSERT INTO deleted_students(

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

        # DELETE FROM MAIN TABLE
        cursor.execute("""
            DELETE FROM students
            WHERE roll_no=?
        """, (roll_no,))

        # SAVE CHANGES
        conn.commit()

        # SUCCESS MESSAGE
        success_message("Student Deleted Successfully")

    # HANDLE GENERAL ERRORS
    except Exception as error:
        if conn:
            conn.rollback()
        error_message(f"Something Went Wrong: {error}")

    # CLOSE CONNECTION
    finally:
        close_connection(conn, cursor)