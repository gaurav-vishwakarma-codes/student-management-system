from database.db_connection import (
    get_connection,
    close_connection
)

from utils.password_helper import hash_password

from utils.messages import (
    success_message,
    error_message
)

from utils.validations import validate_username, validate_password
from utils.input_helper import get_valid_input

def register_admin():

    conn = None
    cursor = None

    try:

        # REGISTRATION HEADING
        print("\n========== Register Admin ==========")

        # INPUTS
        username = get_valid_input(
            "\nEnter Username: ",
            validate_username
        )

        password = get_valid_input(
            "Enter Password: ",
            validate_password
        )

        # HASH PASSWORD
        hashed_password = hash_password(password)

        # DATABASE CONNECTION
        conn, cursor = get_connection()

        # SAFETY CHECK
        if conn is None or cursor is None:
            error_message("Database Connection Failed")
            return False

        # CHECK EXISTING USERNAME
        cursor.execute("""
            SELECT 1
            FROM admins
            WHERE username=?
        """, (username,))

        if cursor.fetchone():
            error_message("Username Already Exists")
            return

        # INSERT ADMIN
        cursor.execute("""
            INSERT INTO admins(
                username,
                password
            ) VALUES (?, ?)
        """, (username,hashed_password))

        # SAVE CHANGES
        conn.commit()

        # SUCCESS MESSAGE
        success_message(
            "Admin Registered Successfully"
        )

    # HANDLE GENERAL ERRORS
    except Exception as error:
        if conn:
            conn.rollback()
        error_message(
            f"Something Went Wrong: {error}"
        )

    # CLOSE CONNECTION
    finally:
        close_connection(conn, cursor)