# =====================================================
# Update Student Actions
# All database update operations for student records
# Called from app/routes/student_routes.py
#
# ADAPTED FROM THE TKINTER VERSION:
# The original functions took a `window` + `refresh_callback`
# and called messagebox.showerror/showinfo directly. In a web
# app there's no window to parent a popup to and no in-process
# callback to refresh a Treeview — instead every function now
# simply returns (success: bool, message: str) and the calling
# route flashes the message and redirects/re-renders the page.
# =====================================================

from app.database.db_connection import (
    get_connection,
    close_connection
)

from app.services.validations import (
    validate_name,
    validate_age,
    validate_gender,
    validate_course,
    validate_email,
    validate_phone,
    validate_address
)

from app.services.update_helper import (
    store_update_history,
    is_same_value
)


# =====================================================
# UPDATE NAME
# =====================================================

def update_name(old_data, roll_no, new_name):

    name_error = validate_name(new_name)
    if name_error:
        return False, name_error

    if is_same_value(old_data["full_name"], new_name):
        return False, "Name is the same as before."

    conn = None; cursor = None

    try:
        conn, cursor = get_connection()

        store_update_history(cursor, old_data, "Name", new_name)

        cursor.execute(
            "UPDATE students SET full_name = ? WHERE roll_no = ?",
            (new_name, roll_no)
        )

        conn.commit()

        return True, "Name Updated Successfully"

    except Exception as e:
        if conn: conn.rollback()
        return False, str(e)

    finally:
        close_connection(conn, cursor)


# =====================================================
# UPDATE AGE
# =====================================================

def update_age(old_data, roll_no, age):

    age_error = validate_age(age)
    if age_error:
        return False, age_error

    new_age = int(age)

    if is_same_value(old_data["age"], new_age):
        return False, "Age is the same as before."

    conn = None; cursor = None

    try:
        conn, cursor = get_connection()

        store_update_history(cursor, old_data, "Age", new_age)

        cursor.execute(
            "UPDATE students SET age = ? WHERE roll_no = ?",
            (new_age, roll_no)
        )

        conn.commit()

        return True, "Age Updated Successfully"

    except Exception as e:
        if conn: conn.rollback()
        return False, str(e)

    finally:
        close_connection(conn, cursor)


# =====================================================
# UPDATE GENDER
# =====================================================

def update_gender(old_data, roll_no, new_gender):

    gender_error = validate_gender(new_gender)
    if gender_error:
        return False, gender_error

    if is_same_value(old_data["gender"], new_gender):
        return False, "Gender is the same as before."

    conn = None; cursor = None

    try:
        conn, cursor = get_connection()

        store_update_history(cursor, old_data, "Gender", new_gender)

        cursor.execute(
            "UPDATE students SET gender = ? WHERE roll_no = ?",
            (new_gender, roll_no)
        )

        conn.commit()

        return True, "Gender Updated Successfully"

    except Exception as e:
        if conn: conn.rollback()
        return False, str(e)

    finally:
        close_connection(conn, cursor)


# =====================================================
# UPDATE COURSE
# =====================================================

def update_course(old_data, roll_no, new_course):

    course_error = validate_course(new_course)
    if course_error:
        return False, course_error

    if is_same_value(old_data["course"], new_course):
        return False, "Course is the same as before."

    conn = None; cursor = None

    try:
        conn, cursor = get_connection()

        store_update_history(cursor, old_data, "Course", new_course)

        cursor.execute(
            "UPDATE students SET course = ? WHERE roll_no = ?",
            (new_course, roll_no)
        )

        conn.commit()

        return True, "Course Updated Successfully"

    except Exception as e:
        if conn: conn.rollback()
        return False, str(e)

    finally:
        close_connection(conn, cursor)


# =====================================================
# UPDATE EMAIL
# =====================================================

def update_email(old_data, roll_no, new_email):

    email_error = validate_email(new_email)
    if email_error:
        return False, email_error

    if is_same_value(old_data["email"], new_email):
        return False, "Email is the same as before."

    conn = None; cursor = None

    try:
        conn, cursor = get_connection()

        # CHECK FOR DUPLICATE EMAIL (EXCLUDING CURRENT STUDENT)
        cursor.execute(
            "SELECT 1 FROM students WHERE email = ? AND roll_no != ?",
            (new_email, roll_no)
        )

        if cursor.fetchone():
            return False, "Email Already Exists"

        store_update_history(cursor, old_data, "Email", new_email)

        cursor.execute(
            "UPDATE students SET email = ? WHERE roll_no = ?",
            (new_email, roll_no)
        )

        conn.commit()

        return True, "Email Updated Successfully"

    except Exception as e:
        if conn: conn.rollback()
        return False, str(e)

    finally:
        close_connection(conn, cursor)


# =====================================================
# UPDATE PHONE
# =====================================================

def update_phone(old_data, roll_no, new_phone):

    phone_error = validate_phone(new_phone)
    if phone_error:
        return False, phone_error

    if is_same_value(old_data["phone"], new_phone):
        return False, "Phone is the same as before."

    conn = None; cursor = None

    try:
        conn, cursor = get_connection()

        store_update_history(cursor, old_data, "Phone", new_phone)

        cursor.execute(
            "UPDATE students SET phone = ? WHERE roll_no = ?",
            (new_phone, roll_no)
        )

        conn.commit()

        return True, "Phone Updated Successfully"

    except Exception as e:
        if conn: conn.rollback()
        return False, str(e)

    finally:
        close_connection(conn, cursor)


# =====================================================
# UPDATE ADDRESS
# =====================================================

def update_address(old_data, roll_no, new_address):

    address_error = validate_address(new_address)
    if address_error:
        return False, address_error

    if is_same_value(old_data["address"], new_address):
        return False, "Address is the same as before."

    conn = None; cursor = None

    try:
        conn, cursor = get_connection()

        store_update_history(cursor, old_data, "Address", new_address)

        cursor.execute(
            "UPDATE students SET address = ? WHERE roll_no = ?",
            (new_address, roll_no)
        )

        conn.commit()

        return True, "Address Updated Successfully"

    except Exception as e:
        if conn: conn.rollback()
        return False, str(e)

    finally:
        close_connection(conn, cursor)


# =====================================================
# UPDATE ALL FIELDS
# =====================================================

def update_all(old_data, roll_no, fields):
    """
    fields: dict with keys —
        new_name, age, new_gender, new_course,
        new_email, new_phone, new_address
    Returns (success: bool, message: str)
    """

    new_name    = fields["new_name"]
    age         = fields["age"]
    new_gender  = fields["new_gender"]
    new_course  = fields["new_course"]
    new_email   = fields["new_email"]
    new_phone   = fields["new_phone"]
    new_address = fields["new_address"]

    # VALIDATE ALL FIELDS FIRST
    validation_errors = [
        validate_name(new_name),
        validate_age(age),
        validate_gender(new_gender),
        validate_course(new_course),
        validate_email(new_email),
        validate_phone(new_phone),
        validate_address(new_address)
    ]

    for error in validation_errors:
        if error:
            return False, error

    new_age = int(age)

    conn = None; cursor = None

    try:
        conn, cursor = get_connection()

        # CHECK DUPLICATE EMAIL (EXCLUDING CURRENT STUDENT)
        cursor.execute(
            "SELECT 1 FROM students WHERE email = ? AND roll_no != ?",
            (new_email, roll_no)
        )

        if cursor.fetchone():
            return False, "Email Already Exists"

        # LOG THE UPDATE WITH ALL OLD VALUES
        store_update_history(
            cursor, old_data,
            "All Fields", "Multiple Fields Updated"
        )

        # UPDATE ALL FIELDS IN ONE QUERY
        cursor.execute("""
            UPDATE students
            SET full_name = ?, age = ?, gender = ?,
                course = ?, email = ?, phone = ?, address = ?
            WHERE roll_no = ?
        """, (
            new_name, new_age, new_gender, new_course,
            new_email, new_phone, new_address, roll_no
        ))

        conn.commit()

        return True, "All Fields Updated Successfully"

    except Exception as e:
        if conn: conn.rollback()
        return False, str(e)

    finally:
        close_connection(conn, cursor)