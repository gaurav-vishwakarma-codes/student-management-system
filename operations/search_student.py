from database.db_connection import (
    get_connection,
    close_connection
)

from utils.db_helper import is_table_empty

from utils.input_helper import get_valid_input

from utils.validations import (
    validate_roll_no,
    validate_search_name,
    validate_search_course,
    validate_search_gender,
    validate_search_email
)

from utils.messages import (
    success_message,
    error_message
)

from utils.display_helper import display_student

from utils.pagination_helper import paginate_records

def search_student():

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
        cursor.execute("SELECT * FROM students")
        total_students = cursor.fetchall()

        # IF ONLY ONE STUDENT EXISTS
        if len(total_students ) == 1:
            paginate_records(
                        total_students,
                        display_student
                    )
            return
        else:
            success_message(f"Total Records Available: {len(total_students)}")
        
        # SEARCH MENU LOOP
        while True:

            # SEARCH MENU
            print("\n========== Search Menu ==========")

            print("1. Search By Roll Number")
            print("2. Search By Name")
            print("3. Search By Course")
            print("4. Search By Gender")
            print("5. Search By Email")
            print("6. Exit Search")

            choice = input(
                "\nEnter Your Choice: "
            ).strip()

            # SEARCH BY ROLL NUMBER
            if choice == "1":

                roll_no = int(
                    get_valid_input(
                        "\nEnter Roll Number: ",
                        validate_roll_no
                    )
                )
                
                # search specific student
                cursor.execute("""
                    SELECT *
                    FROM students
                    WHERE roll_no=?
                """, (roll_no,))

                student = cursor.fetchone()

                if student:
                    success_message(
                        "Student Found"
                    )
                    # SINGLE RECORD → DIRECT DISPLAY
                    display_student(student)
                else:
                    error_message("Student Not Found")

            # SEARCH BY NAME
            elif choice == "2":

                name = get_valid_input(
                    "\nEnter Student Name: ",
                    validate_search_name
                )

                cursor.execute("""
                    SELECT *
                    FROM students
                    WHERE full_name LIKE ?
                """, ('%' + name + '%',))

                students = cursor.fetchall()

                if students:
                    success_message(
                        "Search Results"
                    )
                    paginate_records(
                        students,
                        display_student
                    )
                else:
                    error_message("Student Not Found")

            # SEARCH BY COURSE
            elif choice == "3":

                course = get_valid_input(
                    "\nEnter Course Name: ",
                    validate_search_course
                )

                cursor.execute("""
                    SELECT *
                    FROM students
                    WHERE course LIKE ?
                """, ('%' + course + '%',))

                students = cursor.fetchall()

                if students:
                    success_message(
                        "Search Results"
                    )
                    paginate_records(
                        students,
                        display_student
                    )
                else:
                    error_message("Student Not Found")

            # SEARCH BY GENDER
            elif choice == "4":

                gender = get_valid_input(
                    "\nEnter Gender: ",
                    validate_search_gender
                )

                cursor.execute("""
                    SELECT *
                    FROM students
                    WHERE gender LIKE ?
                """, ('%' + gender + '%',))

                students = cursor.fetchall()

                if students:
                    success_message(
                        "Search Results"
                    )
                    paginate_records(
                        students,
                        display_student
                    )
                else:
                    error_message("Student Not Found")

            # SEARCH BY EMAIL
            elif choice == "5":

                email = get_valid_input(
                    "\nEnter Email: ",
                    validate_search_email
                )

                cursor.execute("""
                    SELECT *
                    FROM students
                    WHERE email LIKE ?
                """, ('%' + email + '%',))

                students = cursor.fetchall()

                if students:
                    success_message(
                        "Student Found"
                    )
                    paginate_records(
                        students,
                        display_student
                    )
                else:
                    error_message("Student Not Found")
            
            # EXIT SEARCH
            elif choice == "6":
                success_message(
                    "Exited Search Menu"
                )
                break

            # INVALID CHOICE
            else:
                error_message("Please Enter Number Between 1-6")

    # HANDLE GENERAL ERRORS
    except Exception as error:
        error_message(
            f"Something Went Wrong: {error}"
        )

    # CLOSE CONNECTION
    finally:
        close_connection(conn, cursor)