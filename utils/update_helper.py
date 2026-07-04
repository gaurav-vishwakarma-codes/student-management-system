# =====================================================
# Update Helper
# Helper functions used during student update operations
# =====================================================


# =====================================================
# CHECK IF VALUE IS SAME (NO CHANGE)
# =====================================================

def is_same_value(old_value, new_value):
    """
    Compares old and new values to detect if anything actually changed.
    - For strings: comparison is case-insensitive and strips whitespace
    - For non-strings (e.g. integers): direct equality check
    Returns True if values are the same (no change), False otherwise.
    """

    # HANDLE STRING VALUES (case-insensitive comparison)
    if isinstance(old_value, str) and isinstance(new_value, str):

        if old_value.strip().lower() == new_value.strip().lower():
            return True

    # HANDLE NON-STRING VALUES (int, float, etc.)
    else:

        if old_value == new_value:
            return True

    return False


# =====================================================
# STORE UPDATE HISTORY
# =====================================================

def store_update_history(cursor, old_data, updated_field, new_value):
    """
    Inserts a record into the updated_students table
    before applying the update to the students table.
    Captures a full snapshot of the student's old data
    along with which field was changed and the new value.
    """

    cursor.execute("""
        INSERT INTO updated_students (

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