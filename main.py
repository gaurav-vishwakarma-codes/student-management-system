# =====================================================
# Student Management System (Tkinter + SQLite)
# Main Entry Point — execution starts here
# =====================================================

import tkinter as tk

# DATABASE INITIALIZATION
from database.db_creation import create_tables

# START WINDOW (first screen shown)
from gui.start_window import StartWindow


# =====================================================
# MAIN FUNCTION
# =====================================================

def main():

    # CREATE ALL DATABASE TABLES (if not already created)
    create_tables()

    # CREATE MAIN TKINTER ROOT WINDOW
    root = tk.Tk()

    # LAUNCH START PAGE (Login / Register screen)
    StartWindow(root)

    # START THE GUI EVENT LOOP (keeps window open)
    root.mainloop()


# =====================================================
# PROGRAM ENTRY POINT
# =====================================================

if __name__ == "__main__":
    main()