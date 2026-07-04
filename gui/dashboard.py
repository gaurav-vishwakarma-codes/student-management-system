# =====================================================
# Dashboard Window
# Main control panel shown after successful login
# All student management features are accessed here
# =====================================================

import tkinter as tk
from tkinter import messagebox

from gui.add_student_window          import AddStudentWindow
from gui.view_students_window        import ViewStudentsWindow
from gui.search_student_window       import SearchStudentWindow
from gui.update_student_window       import UpdateStudentWindow
from gui.delete_student_window       import DeleteStudentWindow
from gui.view_updated_history_window import UpdatedHistoryWindow
from gui.view_deleted_history_window import DeletedHistoryWindow

from database.dummy_data import (
    insert_dummy_students,
    is_table_empty
)


class Dashboard:

    def __init__(self, root):

        self.root = root

        # ==========================================
        # WINDOW SETTINGS
        # ==========================================

        self.root.title("Student Management System")
        self.root.geometry("500x470")
        self.root.resizable(False, False)

        # ==========================================
        # HEADING
        # ==========================================

        tk.Label(
            root,
            text="Student Management System",
            font=("Arial", 16, "bold")
        ).pack(pady=20)

        # ==========================================
        # NAVIGATION BUTTONS
        # Each button opens its respective window
        # ==========================================

        tk.Button(
            root,
            text="Load Dummy Data",
            width=30,
            font=("Arial", 11),
            command=self.load_dummy_data
        ).pack(pady=5)

        tk.Button(
            root,
            text="Add Student",
            width=30,
            font=("Arial", 11),
            command=self.add_student
        ).pack(pady=5)

        tk.Button(
            root,
            text="View Students",
            width=30,
            font=("Arial", 11),
            command=self.view_students
        ).pack(pady=5)

        tk.Button(
            root,
            text="Search Student",
            width=30,
            font=("Arial", 11),
            command=self.search_student
        ).pack(pady=5)

        tk.Button(
            root,
            text="Update Student",
            width=30,
            font=("Arial", 11),
            command=self.update_student
        ).pack(pady=5)

        tk.Button(
            root,
            text="Delete Student",
            width=30,
            font=("Arial", 11),
            command=self.delete_student
        ).pack(pady=5)

        tk.Button(
            root,
            text="Updated Students History",
            width=30,
            font=("Arial", 11),
            command=self.updated_history
        ).pack(pady=5)

        tk.Button(
            root,
            text="Deleted Students History",
            width=30,
            font=("Arial", 11),
            command=self.deleted_history
        ).pack(pady=5)

        tk.Button(
            root,
            text="Exit",
            width=30,
            font=("Arial", 11),
            command=self.exit_program
        ).pack(pady=15)

    # ==========================================
    # BUTTON HANDLER FUNCTIONS
    # ==========================================

    def add_student(self):
        # OPEN ADD STUDENT WINDOW
        AddStudentWindow(self.root)

    def view_students(self):
        # OPEN VIEW STUDENTS WINDOW
        ViewStudentsWindow(self.root)

    def search_student(self):
        # OPEN SEARCH STUDENT WINDOW
        SearchStudentWindow(self.root)

    def update_student(self):
        # OPEN UPDATE STUDENT WINDOW
        UpdateStudentWindow(self.root)

    def delete_student(self):
        # OPEN DELETE STUDENT WINDOW
        DeleteStudentWindow(self.root)

    def updated_history(self):
        # OPEN UPDATED HISTORY WINDOW
        UpdatedHistoryWindow(self.root)

    def deleted_history(self):
        # OPEN DELETED HISTORY WINDOW
        DeletedHistoryWindow(self.root)

    def load_dummy_data(self):
        """
        Inserts 100 dummy student records only if the table is empty.
        Prevents duplicate insertions if data already exists.
        """

        if is_table_empty():

            success = insert_dummy_students()

            if success:
                messagebox.showinfo(
                    "Success",
                    "100 dummy student records inserted successfully."
                )
            else:
                messagebox.showerror(
                    "Error",
                    "Failed to insert dummy student records."
                )

        else:

            # TABLE ALREADY HAS DATA — SKIP INSERTION
            messagebox.showwarning(
                "Data Exists",
                "Student table already contains records."
            )

    def exit_program(self):
        # CLOSE THE APPLICATION
        self.root.destroy()