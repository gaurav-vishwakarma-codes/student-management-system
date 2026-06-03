from utils.messages import success_message

# ==========================================
# CHECK IF VALUE IS CHANGED
# ==========================================

def is_same_value(old_value, new_value):

    # HANDLE STRING VALUES
    if isinstance(old_value, str) and isinstance(new_value, str):

        if old_value.strip().lower() == new_value.strip().lower():

            success_message(
                "No Changes Detected"
            )

            return True

    # HANDLE NON-STRING VALUES
    else:

        if old_value == new_value:

            success_message(
                "No Changes Detected"
            )

            return True

    return False


# ==========================================
# REFRESH STUDENT DATA
# ==========================================

def get_student(cursor, roll_no):

    cursor.execute("""
        SELECT *
        FROM students
        WHERE roll_no=?
    """, (roll_no,))

    return cursor.fetchone()

# STORE UPDATE HISTORY
def store_update_history(cursor, old_data, updated_field, new_value):

    cursor.execute("""
        INSERT INTO updated_students(

            roll_no,
            old_full_name,
            old_age,
            old_gender,
            old_course,
            old_email,
            old_phone,
            old_address,
            updated_field,
            new_value

        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        old_data["roll_no"],
        old_data["full_name"],
        old_data["age"],
        old_data["gender"],
        old_data["course"],
        old_data["email"],
        old_data["phone"],
        old_data["address"],
        updated_field,
        str(new_value)
    ))