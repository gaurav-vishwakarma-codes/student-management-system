from database.db_connection import (
    get_connection,
    close_connection
)

from utils.password_helper import verify_password

from utils.messages import (
    success_message,
    error_message
)

from utils.validations import validate_username, validate_password
from utils.input_helper import get_valid_input

def admin_login():

    conn = None
    cursor = None

    try:

        # LOGIN HEADING
        print("\n========== Admin Login ==========")

        # INPUTS
        username = get_valid_input(
            "\nEnter Username: ",
            validate_username
        )

        password = get_valid_input(
            "Enter Password: ",
            validate_password
        )

        conn, cursor = get_connection()

        if conn is None or cursor is None:
            error_message("Database Connection Failed")
            return False
        
        # fetching password
        cursor.execute("""
            SELECT password
            FROM admins
            WHERE username=?
        """, (username,))
        
        admin = cursor.fetchone()

        # CHECK USERNAME
        if admin is None:
            error_message("Invalid Username")
            return False

        # STORED PASSWORD
        stored_password = admin["password"]

        if verify_password(password,stored_password):
            success_message(
                "Login Successful"
            )
            return True

        else:
            error_message(
                "Invalid Password"
            )
            return False

    # HANDLE GENERAL ERRORS
    except Exception as error:
        error_message(
            f"Something Went Wrong: {error}"
        )
        return False

    # CLOSE CONNECTION
    finally:
        close_connection(conn, cursor)