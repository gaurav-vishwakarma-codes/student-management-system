from database.db_connection import (
    get_connection,
    close_connection
)

from utils.validations import (

    validate_roll_no,
    validate_name,
    validate_age,
    validate_gender,
    validate_course,
    validate_email,
    validate_phone,
    validate_address

)

from utils.input_helper import get_valid_input

from utils.messages import (
    success_message,
    error_message
)


def add_student():

    conn = None
    cursor = None

    try:
        # DATABASE CONNECTION
        conn, cursor = get_connection()
        
        # ❌ SAFETY CHECK (IMPORTANT FIX)
        if conn is None or cursor is None:
            error_message("Database connection failed")
            return
        
        # INPUTS WITH VALIDATIONS
        
        # ROLL NUMBER
        while True:
            roll_no = int(
                get_valid_input(
                    "\nEnter Roll Number: ",
                    validate_roll_no
                )
            )

            # CHECK DUPLICATE ROLL NUMBER
            cursor.execute("""
                SELECT 1
                FROM students
                WHERE roll_no=?
            """, (roll_no,))

            if cursor.fetchone():
                error_message("Roll Number Already Exists")
            else:
                break

        # FULL NAME
        full_name = get_valid_input(
            "\nEnter Full Name: ",
            validate_name
        )
        
        # AGE
        age = int(
            get_valid_input(
                "\nEnter Age: ",
                validate_age
            )
        )

        # GENDER
        gender = get_valid_input(
            "\nEnter Gender: ",
            validate_gender
        )

        # COURSE
        course = get_valid_input(
            "\nEnter Course: ",
            validate_course
        )

        # EMAIL
        while True:

            email = get_valid_input(
                "\nEnter Email: ",
                validate_email
            )

            # CHECK DUPLICATE EMAIL
            cursor.execute("""
                SELECT 1
                FROM students
                WHERE email=?
            """, (email,))

            if cursor.fetchone():
                error_message("Email Already Exists")
            else:
                break
        
        # PHONE
        phone = get_valid_input(
            "\nEnter Phone Number: ",
            validate_phone
        )

        # ADDRESS
        address = get_valid_input(
            "\nEnter Address: ",
            validate_address
        )

        # INSERT STUDENT
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

            roll_no,
            full_name,
            age,
            gender,
            course,
            email,
            phone,
            address

        ))

        # SAVE CHANGES
        conn.commit()

        # SUCCESS MESSAGE
        success_message("Student Added Successfully")

    # HANDLE GENERAL ERRORS
    except Exception as error:
        if conn:
            conn.rollback()
        error_message(f"Something Went Wrong: {error}")

    # CLOSE CONNECTION
    finally:
        close_connection(conn, cursor)