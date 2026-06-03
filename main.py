import time, sys

# DATABASE INITIALIZATION
from database.db_creation import create_tables

# UTILS IMPORTS
from utils.messages import *

# OPERATIONS IMPORTS
from operations.register_admin import register_admin
from operations.login import admin_login
from operations.add_student import add_student
from operations.view_students import view_students
from operations.search_student import search_student
from operations.update_student import update_student
from operations.delete_student import delete_student

from operations.history import (
    view_updated_history,
    view_deleted_history,
    restore_deleted_student
)

# MAIN MENU FUNCTION
def display_menu():

    print("\n========== Student Management System ==========")

    print("1. Add Student")
    print("2. View Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. View Updated Students History")
    print("7. View Deleted Students History")
    print("8. Restore Deleted Student")
    print("9. Exit")

# AUTH MENU FUNCTION
def auth_menu():

    print("\n========== Welcome ==========")

    print("1. Register Admin")
    print("2. Login")
    print("3. Exit")

create_tables() # table create as project main file run

# AUTHENTICATION LOOP
while True:

    auth_menu()

    choice = input(
        "\nEnter Your Choice: "
    ).strip()

    # REGISTER ADMIN
    if choice == "1":
        register_admin()

    # LOGIN
    elif choice == "2":

        if admin_login():

            success_message(
                "Access Granted"
            )

            break

        else:

            error_message(
                "Access Denied"
            )

    # EXIT
    elif choice == "3":

        success_message(
            "Exiting Program..."
        )

        time.sleep(2)

        sys.exit()

    # INVALID CHOICE
    else:

        error_message("Invalid Choice")

        error_message(
            "Please Enter Number Between 1-3"
        )

# MAIN PROGRAM LOOP
while True:

    display_menu()

    choice = input("\nEnter Your Choice: ")

    # ADD STUDENT
    if choice == "1":
        add_student()

    # VIEW STUDENTS
    elif choice == "2":
        view_students()

    # SEARCH STUDENT
    elif choice == "3":
        search_student()

    # UPDATE STUDENT
    elif choice == "4":
        update_student()

    # DELETE STUDENT
    elif choice == "5":
        delete_student()

    # VIEW UPDATED HISTORY
    elif choice == "6":
        view_updated_history()

    # VIEW DELETED HISTORY
    elif choice == "7":
        view_deleted_history()

    # RESTORE DELETED STUDENT
    elif choice == "8":
        restore_deleted_student()

    # EXIT
    elif choice == "9":

        success_message("Exiting Student Management System...")

        time.sleep(2)

        success_message("Thank You")

        break

    # INVALID INPUT
    else:

        error_message("Invalid Choice")

        error_message("Please Enter Number Between 1-9")