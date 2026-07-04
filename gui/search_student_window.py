# =====================================================
# Search for a student record by Roll Number
# DB work is delegated to utils/student_service.py
# =====================================================

import tkinter as tk
from tkinter import ttk, messagebox

import utils.student_service as student_service

from utils.validations import validate_roll_no


class SearchStudentWindow:

    def __init__(self, parent):

        self.window = tk.Toplevel(parent)

        # ==========================================
        # WINDOW SETTINGS
        # ==========================================

        self.window.title("Search Student")
        self.window.geometry("1000x450")
        self.window.resizable(False, False)
        self.window.focus_force()

        # ==========================================
        # HEADING
        # ==========================================

        tk.Label(
            self.window,
            text="Search Student By Roll Number",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        # ==========================================
        # SEARCH FIELD (Roll Number entry + button)
        # ==========================================

        search_frame = tk.Frame(self.window)
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="Roll Number:", font=("Arial", 11)).grid(row=0, column=0, padx=5)

        self.roll_entry = tk.Entry(search_frame, width=20, font=("Arial", 11))
        self.roll_entry.grid(row=0, column=1, padx=5, ipady=2)

        tk.Button(
            search_frame,
            text="Search",
            font=("Arial", 11),
            command=self.search_student
        ).grid(row=0, column=2, padx=5)

        # ==========================================
        # TABLE COLUMNS
        # ==========================================

        columns = (
            "Roll No", "Full Name", "Age", "Gender",
            "Course", "Email", "Phone", "Address"
        )

        # ==========================================
        # TREEVIEW — displays the matched student
        # ==========================================

        self.tree = ttk.Treeview(self.window, columns=columns, show="headings")
        
        # SET COLUMN HEADINGS AND WIDTHS
        widths = {
            "Roll No": 80, "Full Name": 150, "Age": 60, "Gender": 80,
            "Course": 120, "Email": 200, "Phone": 120, "Address": 220
        }

        for heading in columns:
            self.tree.heading(heading, text=heading)
            anchor = "center" if heading in ("Roll No", "Age", "Gender") else "w"
            self.tree.column(heading, width=widths[heading], anchor=anchor)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    # ==========================================
    # SEARCH STUDENT BY ROLL NUMBER
    # ==========================================

    def search_student(self):

        roll_no = self.roll_entry.get().strip()
        
        # VALIDATE ROLL NUMBER FORMAT
        roll_no_error = validate_roll_no(roll_no)

        if roll_no_error:
            messagebox.showerror("Invalid Roll Number", roll_no_error, parent=self.window)
            return

        try:

            student = student_service.get_student_by_roll(int(roll_no))
            
            # CLEAR ANY PREVIOUS RESULT BEFORE SHOWING NEW ONE
            for item in self.tree.get_children():
                self.tree.delete(item)

            if student is None:
                messagebox.showinfo("Not Found", "No Student Found", parent=self.window)
                return
            
            # INSERT THE MATCHED STUDENT AS A ROW
            self.tree.insert("", "end", values=(
                student["roll_no"],
                student["full_name"],
                student["age"],
                student["gender"],
                student["course"],
                student["email"],
                student["phone"],
                student["address"]
            ))

        except Exception as error:

            messagebox.showerror("Error", str(error), parent=self.window)