def is_table_empty(cursor, table_name):

    allowed_tables = {
        "students",
        "updated_students",
        "deleted_students"
    }

    if table_name not in allowed_tables:
        raise ValueError(f"Invalid table name: {table_name}")

    query = f"SELECT COUNT(*) FROM {table_name}"
    cursor.execute(query)

    count = cursor.fetchone()[0]

    return count == 0