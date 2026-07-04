# =====================================================
# Update Student Actions
# All database update operations for student records
# Called from gui/update_student_window.py
# =====================================================

from tkinter import messagebox

from database.db_connection import (
    get_connection,
    close_connection
)

from utils.validations import (
    validate_name,
    validate_age,
    validate_gender,
    validate_course,
    validate_email,
    validate_phone,
    validate_address
)

from utils.update_helper import (
    store_update_history,
    is_same_value
)


# =====================================================
# UPDATE NAME
# =====================================================

def update_name(window, old_data, roll_no, new_name, refresh_callback):

    name_error = validate_name(new_name)
    if name_error:
        messagebox.showerror("Invalid Name", name_error, parent=window)
        return

    if is_same_value(old_data["full_name"], new_name):
        messagebox.showwarning("No Change", "Name is the same as before.", parent=window)
        return

    conn = None; cursor = None

    try:
        conn, cursor = get_connection()

        store_update_history(cursor, old_data, "Name", new_name)

        cursor.execute(
            "UPDATE students SET full_name = ? WHERE roll_no = ?",
            (new_name, roll_no)
        )

        conn.commit()

        messagebox.showinfo("Success", "Name Updated Successfully", parent=window)

        refresh_callback()

    except Exception as e:
        if conn: conn.rollback()
        messagebox.showerror("Error", str(e), parent=window)

    finally:
        close_connection(conn, cursor)


# =====================================================
# UPDATE AGE
# =====================================================

def update_age(window, old_data, roll_no, age, refresh_callback):

    age_error = validate_age(age)
    if age_error:
        messagebox.showerror("Invalid Age", age_error, parent=window)
        return

    new_age = int(age)

    if is_same_value(old_data["age"], new_age):
        messagebox.showwarning("No Change", "Age is the same as before.", parent=window)
        return

    conn = None; cursor = None

    try:
        conn, cursor = get_connection()

        store_update_history(cursor, old_data, "Age", new_age)

        cursor.execute(
            "UPDATE students SET age = ? WHERE roll_no = ?",
            (new_age, roll_no)
        )

        conn.commit()

        messagebox.showinfo("Success", "Age Updated Successfully", parent=window)

        refresh_callback()

    except Exception as e:
        if conn: conn.rollback()
        messagebox.showerror("Error", str(e), parent=window)

    finally:
        close_connection(conn, cursor)


# =====================================================
# UPDATE GENDER
# =====================================================

def update_gender(window, old_data, roll_no, new_gender, refresh_callback):

    gender_error = validate_gender(new_gender)
    if gender_error:
        messagebox.showerror("Invalid Gender", gender_error, parent=window)
        return

    if is_same_value(old_data["gender"], new_gender):
        messagebox.showwarning("No Change", "Gender is the same as before.", parent=window)
        return

    conn = None; cursor = None

    try:
        conn, cursor = get_connection()

        store_update_history(cursor, old_data, "Gender", new_gender)

        cursor.execute(
            "UPDATE students SET gender = ? WHERE roll_no = ?",
            (new_gender, roll_no)
        )

        conn.commit()

        messagebox.showinfo("Success", "Gender Updated Successfully", parent=window)

        refresh_callback()

    except Exception as e:
        if conn: conn.rollback()
        messagebox.showerror("Error", str(e), parent=window)

    finally:
        close_connection(conn, cursor)


# =====================================================
# UPDATE COURSE
# =====================================================

def update_course(window, old_data, roll_no, new_course, refresh_callback):

    course_error = validate_course(new_course)
    if course_error:
        messagebox.showerror("Invalid Course", course_error, parent=window)
        return

    if is_same_value(old_data["course"], new_course):
        messagebox.showwarning("No Change", "Course is the same as before.", parent=window)
        return

    conn = None; cursor = None

    try:
        conn, cursor = get_connection()

        store_update_history(cursor, old_data, "Course", new_course)

        cursor.execute(
            "UPDATE students SET course = ? WHERE roll_no = ?",
            (new_course, roll_no)
        )

        conn.commit()

        messagebox.showinfo("Success", "Course Updated Successfully", parent=window)

        refresh_callback()

    except Exception as e:
        if conn: conn.rollback()
        messagebox.showerror("Error", str(e), parent=window)

    finally:
        close_connection(conn, cursor)


# =====================================================
# UPDATE EMAIL
# =====================================================

def update_email(window, old_data, roll_no, new_email, refresh_callback):

    email_error = validate_email(new_email)
    if email_error:
        messagebox.showerror("Invalid Email", email_error, parent=window)
        return

    if is_same_value(old_data["email"], new_email):
        messagebox.showwarning("No Change", "Email is the same as before.", parent=window)
        return

    conn = None; cursor = None

    try:
        conn, cursor = get_connection()

        # CHECK FOR DUPLICATE EMAIL (EXCLUDING CURRENT STUDENT)
        cursor.execute(
            "SELECT 1 FROM students WHERE email = ? AND roll_no != ?",
            (new_email, roll_no)
        )

        if cursor.fetchone():
            messagebox.showerror("Duplicate Email", "Email Already Exists", parent=window)
            return

        store_update_history(cursor, old_data, "Email", new_email)

        cursor.execute(
            "UPDATE students SET email = ? WHERE roll_no = ?",
            (new_email, roll_no)
        )

        conn.commit()

        messagebox.showinfo("Success", "Email Updated Successfully", parent=window)

        refresh_callback()

    except Exception as e:
        if conn: conn.rollback()
        messagebox.showerror("Error", str(e), parent=window)

    finally:
        close_connection(conn, cursor)


# =====================================================
# UPDATE PHONE
# =====================================================

def update_phone(window, old_data, roll_no, new_phone, refresh_callback):

    phone_error = validate_phone(new_phone)
    if phone_error:
        messagebox.showerror("Invalid Phone", phone_error, parent=window)
        return

    if is_same_value(old_data["phone"], new_phone):
        messagebox.showwarning("No Change", "Phone is the same as before.", parent=window)
        return

    conn = None; cursor = None

    try:
        conn, cursor = get_connection()

        store_update_history(cursor, old_data, "Phone", new_phone)

        cursor.execute(
            "UPDATE students SET phone = ? WHERE roll_no = ?",
            (new_phone, roll_no)
        )

        conn.commit()

        messagebox.showinfo("Success", "Phone Updated Successfully", parent=window)

        refresh_callback()

    except Exception as e:
        if conn: conn.rollback()
        messagebox.showerror("Error", str(e), parent=window)

    finally:
        close_connection(conn, cursor)


# =====================================================
# UPDATE ADDRESS
# =====================================================

def update_address(window, old_data, roll_no, new_address, refresh_callback):

    address_error = validate_address(new_address)
    if address_error:
        messagebox.showerror("Invalid Address", address_error, parent=window)
        return

    if is_same_value(old_data["address"], new_address):
        messagebox.showwarning("No Change", "Address is the same as before.", parent=window)
        return

    conn = None; cursor = None

    try:
        conn, cursor = get_connection()

        store_update_history(cursor, old_data, "Address", new_address)

        cursor.execute(
            "UPDATE students SET address = ? WHERE roll_no = ?",
            (new_address, roll_no)
        )

        conn.commit()

        messagebox.showinfo("Success", "Address Updated Successfully", parent=window)

        refresh_callback()

    except Exception as e:
        if conn: conn.rollback()
        messagebox.showerror("Error", str(e), parent=window)

    finally:
        close_connection(conn, cursor)


# =====================================================
# UPDATE ALL FIELDS
# =====================================================

def update_all(window, old_data, roll_no, fields, refresh_callback):
    """
    fields: dict with keys —
        new_name, age, new_gender, new_course,
        new_email, new_phone, new_address
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
            messagebox.showerror("Validation Error", error, parent=window)
            return

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
            messagebox.showerror("Duplicate Email", "Email Already Exists", parent=window)
            return

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

        messagebox.showinfo("Success", "All Fields Updated Successfully", parent=window)

        refresh_callback()

    except Exception as e:
        if conn: conn.rollback()
        messagebox.showerror("Error", str(e), parent=window)

    finally:
        close_connection(conn, cursor)