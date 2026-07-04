# =====================================================
# Search for a student by Roll Number, then delete
# DB work is delegated to utils/student_service.py
# =====================================================

import tkinter as tk
from tkinter import messagebox

import utils.student_service as student_service

from utils.validations import validate_roll_no


class DeleteStudentWindow:

    def __init__(self, root):

        self.window = tk.Toplevel(root)

        # ==========================================
        # WINDOW SETTINGS
        # ==========================================

        self.window.title("Delete Student")
        self.window.geometry("450x320")
        self.window.resizable(False, False)
        self.window.focus_force()

        # STORES ROLL NO FOUND BY SEARCH (None until valid search)
        self.found_student = None

        self.setup_ui()

    # ==========================================
    # SETUP UI
    # ==========================================

    def setup_ui(self):

        tk.Label(
            self.window,
            text="Delete Student Record",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        tk.Label(self.window, text="Enter Roll No:", font=("Arial", 11)).pack(pady=5)

        self.roll_entry = tk.Entry(self.window, width=30, font=("Arial", 11))
        self.roll_entry.pack(ipady=2)

        tk.Button(
            self.window,
            text="Search Student",
            font=("Arial", 11),
            command=self.search_student
        ).pack(pady=10)

        self.info_label = tk.Label(self.window, text="", fg="blue", font=("Arial", 11))
        self.info_label.pack(pady=5)

        tk.Button(
            self.window,
            text="Delete Student",
            font=("Arial", 11),
            bg="red",
            fg="white",
            command=self.delete_student
        ).pack(pady=10)

        tk.Label(self.window, text="─" * 40, fg="gray").pack()

        self.delete_all_btn = tk.Button(
            self.window,
            text="Delete All Students",
            font=("Arial", 11),
            bg="#8B0000",
            fg="white",
            width=25,
            command=self.delete_all_students
        )
        self.delete_all_btn.pack(pady=10)

        self.toggle_delete_all_btn()

    # ==========================================
    # TOGGLE DELETE ALL BUTTON STATE
    # ==========================================

    def toggle_delete_all_btn(self):

        try:
            count = student_service.count_students()
            self.delete_all_btn.config(state="normal" if count > 0 else "disabled")

        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self.window)

    # ==========================================
    # SEARCH STUDENT BEFORE DELETE
    # ==========================================

    def search_student(self):

        roll = self.roll_entry.get().strip()

        roll_error = validate_roll_no(roll)

        if roll_error:
            messagebox.showerror("Invalid Roll Number", roll_error, parent=self.window)
            return

        try:
            result = student_service.get_student_by_roll(int(roll))

            if result:

                self.found_student = roll

                self.info_label.config(
                    text=(
                        f"Name: {result['full_name']} | "
                        f"Age: {result['age']} | "
                        f"Course: {result['course']}"
                    )
                )

            else:

                self.found_student = None
                self.info_label.config(text="")
                messagebox.showwarning("Not Found", "Student not found", parent=self.window)

        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self.window)

    # ==========================================
    # DELETE STUDENT (SOFT DELETE)
    # ==========================================

    def delete_student(self):

        roll = self.roll_entry.get().strip()

        roll_error = validate_roll_no(roll)

        if roll_error:
            messagebox.showerror("Invalid Roll Number", roll_error, parent=self.window)
            return

        # REQUIRE A SUCCESSFUL SEARCH BEFORE ALLOWING DELETE
        if self.found_student is None or self.found_student != roll:
            messagebox.showwarning(
                "Search Required",
                "Please search and confirm the student exists before deleting.",
                parent=self.window
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this student?",
            parent=self.window
        )

        if not confirm:
            return

        success, message = student_service.delete_student(int(roll))

        if not success:
            messagebox.showerror("Error", message, parent=self.window)
            return

        messagebox.showinfo("Success", message, parent=self.window)

        self.roll_entry.delete(0, tk.END)
        self.info_label.config(text="")
        self.found_student = None

        self.toggle_delete_all_btn()

    # ==========================================
    # DELETE ALL STUDENTS (SOFT DELETE)
    # ==========================================

    def delete_all_students(self):

        confirm = messagebox.askyesno(
            "Confirm Delete All",
            "Are you sure you want to delete ALL students?\n\nThis will move all records to Deleted History.",
            parent=self.window
        )

        if not confirm:
            return

        success, message, count = student_service.delete_all_students()

        if not success:
            box = messagebox.showwarning if count == 0 else messagebox.showerror
            box("No Records" if count == 0 else "Error", message, parent=self.window)
            return

        messagebox.showinfo("Success", message, parent=self.window)

        self.roll_entry.delete(0, tk.END)
        self.info_label.config(text="")
        self.found_student = None
        self.toggle_delete_all_btn()