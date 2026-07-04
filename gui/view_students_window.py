# =====================================================
# Displays all active student records in a table
# DB work is delegated to utils/student_service.py
# =====================================================

import tkinter as tk
from tkinter import ttk, messagebox

import utils.student_service as student_service


class ViewStudentsWindow:

    def __init__(self, parent):

        self.window = tk.Toplevel(parent)

        # ==========================================
        # WINDOW SETTINGS
        # ==========================================

        self.window.title("View Students")
        self.window.geometry("1200x500")
        self.window.focus_force()

        # ==========================================
        # HEADING
        # ==========================================

        tk.Label(
            self.window,
            text="Students Records",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        # ==========================================
        # TABLE FRAME
        # Holds the Treeview + its scrollbars together
        # ==========================================

        table_frame = tk.Frame(self.window)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # ==========================================
        # SCROLLBARS (created before Treeview so they
        # can be linked via yscrollcommand/xscrollcommand)
        # ==========================================

        scrollbar_y = ttk.Scrollbar(table_frame, orient="vertical")
        scrollbar_x = ttk.Scrollbar(table_frame, orient="horizontal")
        
        # ==========================================
        # TABLE COLUMNS
        # ==========================================

        columns = (
            "Roll No", "Full Name", "Age", "Gender",
            "Course", "Email", "Phone", "Address"
        )
        
        # ==========================================
        # TREEVIEW — displays all student records
        # ==========================================

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )
        
        # LINK SCROLLBARS TO TREEVIEW
        scrollbar_y.config(command=self.tree.yview)
        scrollbar_x.config(command=self.tree.xview)

        # ==========================================
        # SET COLUMN HEADINGS AND WIDTHS
        # ==========================================
        
        widths = {
            "Roll No": 80, "Full Name": 180, "Age": 60, "Gender": 80,
            "Course": 120, "Email": 220, "Phone": 120, "Address": 250
        }

        for heading in columns:
            self.tree.heading(heading, text=heading)
            anchor = "center" if heading in ("Roll No", "Age", "Gender") else "w"
            self.tree.column(heading, width=widths[heading], anchor=anchor)
        
        # ==========================================
        # PACK SCROLLBARS + TREEVIEW
        # ==========================================

        scrollbar_y.pack(side="right",  fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True)

        # ==========================================
        # REFRESH BUTTON
        # ==========================================
        
        tk.Button(
            self.window,
            text="Refresh",
            font=("Arial", 11),
            command=self.load_students
        ).pack(pady=10)
        
        # LOAD DATA IMMEDIATELY WHEN WINDOW OPENS
        self.load_students()

    # ==========================================
    # LOAD ALL STUDENTS
    # Clears the table and re-fetches all active
    # student records from the database
    # ==========================================

    def load_students(self):

        try:

            students = student_service.get_all_students()

            # CLEAR EXISTING ROWS BEFORE INSERTING NEW DATA
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # INSERT EACH STUDENT AS A ROW
            for student in students:
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