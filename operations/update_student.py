from database.db_connection import (
    get_connection,
    close_connection
)

from utils.db_helper import is_table_empty

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

from utils.display_helper import display_student

from utils.pagination_helper import paginate_records

from utils.update_helper import is_same_value, store_update_history, get_student


def update_student():

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

            print(f"\nTotal Records Available: {len(total_students)}")
        
            # INPUT ROLL NUMBER
            roll_no = int(
                get_valid_input(
                    "\nEnter Roll Number To Update: ",
                    validate_roll_no
                )
            )

        # FETCH STUDENT
        cursor.execute("""
            SELECT *
            FROM students
            WHERE roll_no=?
        """, (roll_no,))

        old_data = cursor.fetchone()

        # STUDENT NOT FOUND
        if old_data is None:
            error_message("Student Not Found")
            return
        
        # DISPLAY SELECTED STUDENT
        display_student(old_data)
        
        # UPDATE LOOP
        while True:

            # UPDATE MENU
            print("\n========== Update Menu ==========")

            print("1. Update Name")
            print("2. Update Age")
            print("3. Update Gender")
            print("4. Update Course")
            print("5. Update Email")
            print("6. Update Phone")
            print("7. Update Address")
            print("8. Update All Details")
            print("9. Exit Update Menu")

            choice = input(
                "\nEnter Your Choice: "
            ).strip()
            
            # ======================================
            # UPDATE NAME
            # ======================================

            if choice == "1":
                new_name = get_valid_input(
                    "\nEnter Updated Name: ",
                    validate_name
                )

                if is_same_value(
                    old_data["full_name"],
                    new_name
                ):
                    continue

                store_update_history(cursor, old_data, "Name", new_name)

                cursor.execute("""
                    UPDATE students
                    SET full_name=?
                    WHERE roll_no=?
                """, (new_name,roll_no))

                # CHECK UPDATE SUCCESS
                if cursor.rowcount > 0:

                    success_message(
                        "Name Updated Successfully"
                    )
                
                conn.commit()

                old_data = get_student(
                    cursor,
                    roll_no
                )
            
            # ======================================
            # UPDATE AGE
            # ======================================

            elif choice == "2":

                new_age = int(
                    get_valid_input(
                        "\nEnter Updated Age: ",
                        validate_age
                    )
                )

                

                if is_same_value(
                    old_data["age"],
                    new_age
                ):
                    continue
                
                store_update_history(cursor, old_data, "Age", new_age)

                cursor.execute("""
                    UPDATE students
                    SET age=?
                    WHERE roll_no=?
                """, (new_age,roll_no))

                # CHECK UPDATE SUCCESS
                if cursor.rowcount > 0:

                    success_message(
                        "Age Updated Successfully"
                    )
                
                conn.commit()

                old_data = get_student(
                    cursor,
                    roll_no
                )

            # ======================================
            # UPDATE GENDER
            # ======================================

            elif choice == "3":

                new_gender = get_valid_input(
                    "\nEnter Updated Gender: ",
                    validate_gender
                )

                if is_same_value(
                    old_data["gender"],
                    new_gender
                ):
                    continue

                store_update_history(cursor, old_data, "Gender", new_gender)

                cursor.execute("""
                    UPDATE students
                    SET gender=?
                    WHERE roll_no=?
                """, (new_gender,roll_no))

                # CHECK UPDATE SUCCESS
                if cursor.rowcount > 0:

                    success_message(
                        "Gender Updated Successfully"
                    )
                
                conn.commit()

                old_data = get_student(
                    cursor,
                    roll_no
                )

            # ======================================
            # UPDATE COURSE
            # ======================================

            elif choice == "4":

                new_course = get_valid_input(
                    "\nEnter Updated Course: ",
                    validate_course
                )

                if is_same_value(
                    old_data["course"],
                    new_course
                ):
                    continue

                store_update_history(cursor, old_data, "Course", new_course)

                cursor.execute("""
                    UPDATE students
                    SET course=?
                    WHERE roll_no=?
                """, (new_course,roll_no))

                # CHECK UPDATE SUCCESS
                if cursor.rowcount > 0:

                    success_message(
                        "Course Updated Successfully"
                    )
                
                conn.commit()

                old_data = get_student(
                    cursor,
                    roll_no
                )

            # ======================================
            # UPDATE EMAIL
            # ======================================

            elif choice == "5":
                same_email = False

                while True:

                    new_email = get_valid_input(
                        "\nEnter Updated Unique Email: ",
                        validate_email
                    )

                    # SAME EMAIL AS CURRENT RECORD
                    if is_same_value(
                        old_data["email"],
                        new_email
                    ):
                        same_email = True
                        break

                    # CHECK DUPLICATE EMAIL
                    cursor.execute("""
                        SELECT 1
                        FROM students
                        WHERE email=? AND roll_no!=?
                    """, (new_email,roll_no))

                    if cursor.fetchone():
                        error_message(
                            "Email Already Exists"
                        )
                    else:
                        break

                if same_email:
                    continue
                
                store_update_history(cursor, old_data, "Email", new_email)

                cursor.execute("""
                    UPDATE students
                    SET email=?
                    WHERE roll_no=?
                """, (new_email,roll_no))

                # CHECK UPDATE SUCCESS
                if cursor.rowcount > 0:

                    success_message(
                        "Email Updated Successfully"
                    )
                
                conn.commit()

                old_data = get_student(
                    cursor,
                    roll_no
                )

            # ======================================
            # UPDATE PHONE
            # ======================================

            elif choice == "6":

                new_phone = get_valid_input(
                    "\nEnter Updated Phone Number: ",
                    validate_phone
                )

                if is_same_value(
                    old_data["phone"],
                    new_phone
                ):
                    continue

                store_update_history(cursor, old_data, "Phone", new_phone)

                cursor.execute("""
                    UPDATE students
                    SET phone=?
                    WHERE roll_no=?
                """, (new_phone,roll_no))

                # CHECK UPDATE SUCCESS
                if cursor.rowcount > 0:

                    success_message(
                        "Phone Number Updated Successfully"
                    )
                
                conn.commit()

                old_data = get_student(
                    cursor,
                    roll_no
                )

            # ======================================
            # UPDATE ADDRESS
            # ======================================

            elif choice == "7":

                new_address = get_valid_input(
                    "\nEnter Updated Address: ",
                    validate_address
                )

                if is_same_value(
                    old_data["address"],
                    new_address
                ):
                    continue

                store_update_history(cursor, old_data, "Address", new_address)

                cursor.execute("""
                    UPDATE students
                    SET address=?
                    WHERE roll_no=?
                """, (new_address,roll_no))

                # CHECK UPDATE SUCCESS
                if cursor.rowcount > 0:

                    success_message(
                        "Address Updated Successfully"
                    )
                
                conn.commit()

                old_data = get_student(
                    cursor,
                    roll_no
                )

            # ======================================
            # UPDATE ALL DETAILS
            # ======================================

            elif choice == "8":
                
                new_name = get_valid_input(
                    "\nEnter Updated Name: ",
                    validate_name
                )

                new_age = int(
                    get_valid_input(
                        "\nEnter Updated Age: ",
                        validate_age
                    )
                )

                new_gender = get_valid_input(
                    "\nEnter Updated Gender: ",
                    validate_gender
                )

                new_course = get_valid_input(
                    "\nEnter Updated Course: ",
                    validate_course
                )

                # EMAIL VALIDATION + DUPLICATE CHECK
                while True:

                    new_email = get_valid_input(
                        "\nEnter Updated Unique Email: ",
                        validate_email
                    )

                    # CHECK DUPLICATE EMAIL
                    cursor.execute("""
                        SELECT 1
                        FROM students
                        WHERE email=? AND roll_no!=?
                    """, (new_email,roll_no))

                    if cursor.fetchone():
                        error_message("Email Already Exists")
                    else:
                        break

                new_phone = get_valid_input(
                    "\nEnter Updated Phone Number: ",
                    validate_phone
                )

                new_address = get_valid_input(
                    "\nEnter Updated Address: ",
                    validate_address
                )

                store_update_history(cursor, old_data, "All Fields", "Multiple Fields Updated")

                # UPDATE STUDENT
                cursor.execute("""
                    UPDATE students

                    SET

                        full_name=?,
                        age=?,
                        gender=?,
                        course=?,
                        email=?,
                        phone=?,
                        address=?

                    WHERE roll_no=?

                """, (

                    new_name,
                    new_age,
                    new_gender,
                    new_course,
                    new_email,
                    new_phone,
                    new_address,
                    roll_no

                ))
            
                conn.commit()

                print("Row Count =", cursor.rowcount)
            
                # CHECK UPDATE SUCCESS
                if cursor.rowcount > 0:
                    success_message(
                        "Details Updated Successfully"
                    )
                
                old_data = get_student(
                    cursor,
                    roll_no
                )
            
            elif choice == "9":
                success_message("Exited Update Menu")
                break

            else:
                error_message(
                    "Please Enter Number Between 1-9"
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