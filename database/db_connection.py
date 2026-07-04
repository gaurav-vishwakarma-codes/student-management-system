# =====================================================
# Database Connection
# Handles creating and closing SQLite connections
# =====================================================

import sqlite3
from config import DB_NAME

# =====================================================
# GET CONNECTION
# =====================================================

def get_connection():
    """
    Creates and returns a SQLite database connection and cursor.
    Rows are returned as dictionary-like objects (sqlite3.Row),
    so columns can be accessed by name e.g. row['full_name'].
    Returns (None, None) if connection fails.
    """

    try:

        # CONNECT TO DATABASE FILE
        conn = sqlite3.connect(DB_NAME)

        # RETURN ROWS AS DICTIONARY (access columns by name)
        conn.row_factory = sqlite3.Row

        # CREATE CURSOR
        cursor = conn.cursor()

        return conn, cursor

    except sqlite3.Error as error:
        print(f"[DB ERROR] Failed to connect: {error}")
        return None, None


# =====================================================
# CLOSE CONNECTION
# =====================================================

def close_connection(conn, cursor=None):
    """
    Safely closes the cursor and database connection.
    Handles errors silently to avoid crashing the app.
    """

    try:

        # CLOSE CURSOR IF PROVIDED
        if cursor:
            cursor.close()

        # CLOSE CONNECTION IF PROVIDED
        if conn:
            conn.close()

    except sqlite3.Error as error:
        print(f"[DB ERROR] Failed to close connection: {error}")