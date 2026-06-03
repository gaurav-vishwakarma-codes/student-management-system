import sqlite3


def get_connection():
    """
    Creates and returns database connection and cursor safely.
    """
    try:
        conn = sqlite3.connect("student.db")

        # RETURN ROWS AS DICTIONARY (like JSON)
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        return conn, cursor

    except sqlite3.Error as error:
        print(f"[DB ERROR] Failed to connect: {error}")
        return None, None


def close_connection(conn, cursor=None):
    """
    Safely closes database resources.
    """

    try:
        if cursor:
            cursor.close()

        if conn:
            conn.close()

    except sqlite3.Error as error:
        print(f"[DB ERROR] Failed to close connection: {error}")