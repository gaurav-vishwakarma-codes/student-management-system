# =====================================================
# Form to add a new student record to the database
# Validation happens here; DB work is delegated to
# utils/student_service.py
# =====================================================

import tkinter as tk
from tkinter import messagebox

import utils.student_service as student_service

from utils.validations import (
    validate_required_fields,
    validate_roll_no,
    validate_name,
    validate_age,
    validate_gender,
    validate_course,
    validate_email,
    validate_phone,
    validate_address
)


class AddStudentWindow:

    def __init__(self, parent):

        self.window = tk.Toplevel(parent)

        # ==========================================
        # WINDOW SETTINGS
        # ==========================================

        self.window.title("Add Student")
        self.window.geometry("500x580")
        self.window.resizable(False, False)
        self.window.focus_force()

        # ==========================================
        # HEADING
        # ==========================================

        tk.Label(
            self.window,
            text="Add Student",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        # ==========================================
        # INPUT FIELDS
        # ==========================================

        self.roll_entry    = self.create_field("Roll Number")
        self.name_entry    = self.create_field("Full Name")
        self.age_entry     = self.create_field("Age")
        self.gender_entry  = self.create_field("Gender")
        self.course_entry  = self.create_field("Course")
        self.email_entry   = self.create_field("Email")
        self.phone_entry   = self.create_field("Phone Number")
        self.address_entry = self.create_field("Address")

        # ==========================================
        # SUBMIT BUTTON
        # ==========================================

        tk.Button(
            self.window,
            text="Add Student",
            width=20,
            font=("Arial", 11),
            command=self.save_student
        ).pack(pady=15)

    # ==========================================
    # HELPER — CREATE LABEL + ENTRY FIELD
    # ==========================================

    def create_field(self, label):

        tk.Label(self.window, text=label, font=("Arial", 11)).pack()

        entry = tk.Entry(self.window, width=30, font=("Arial", 11))
        entry.pack(pady=5, ipady=2)

        return entry

    # ==========================================
    # SAVE STUDENT
    # Validates all fields then delegates the insert
    # to student_service.add_student()
    # ==========================================

    def save_student(self):

        roll_no   = self.roll_entry.get().strip()
        full_name = self.name_entry.get().strip()
        age       = self.age_entry.get().strip()
        gender    = self.gender_entry.get().strip()
        course    = self.course_entry.get().strip()
        email     = self.email_entry.get().strip()
        phone     = self.phone_entry.get().strip()
        address   = self.address_entry.get().strip()

        # ======================================
        # STEP 1 — REQUIRED FIELDS CHECK
        # ======================================

        student_data = {
            "Roll Number":  roll_no,
            "Full Name":    full_name,
            "Age":          age,
            "Gender":       gender,
            "Course":       course,
            "Email":        email,
            "Phone Number": phone,
            "Address":      address
        }

        missing_fields = validate_required_fields(student_data)

        if missing_fields:
            messagebox.showerror(
                "Required Fields",
                "Please fill the following fields:\n\n"
                + "\n".join(missing_fields),
                parent=self.window
            )
            return

        # ======================================
        # STEP 2 — INDIVIDUAL FIELD VALIDATIONS
        # ======================================

        validators = [
            ("Invalid Roll Number", validate_roll_no(roll_no)),
            ("Invalid Name",        validate_name(full_name)),
            ("Invalid Age",         validate_age(age)),
            ("Invalid Gender",      validate_gender(gender)),
            ("Invalid Course",      validate_course(course)),
            ("Invalid Email",       validate_email(email)),
            ("Invalid Phone Number", validate_phone(phone)),
            ("Invalid Address",     validate_address(address)),
        ]

        for title, error in validators:
            if error:
                messagebox.showerror(title, error, parent=self.window)
                return

        # ======================================
        # STEP 3 — DELEGATE TO SERVICE LAYER
        # ======================================

        success, message = student_service.add_student({
            "roll_no":   int(roll_no),
            "full_name": full_name,
            "age":       int(age),
            "gender":    gender,
            "course":    course,
            "email":     email,
            "phone":     phone,
            "address":   address
        })

        if not success:
            messagebox.showerror("Database Error", message, parent=self.window)
            return

        messagebox.showinfo("Success", message, parent=self.window)

        # KEEP WINDOW IN FRONT AFTER SUCCESS
        self.window.lift()
        self.window.focus_force()

        self.clear_fields()

    # ==========================================
    # CLEAR ALL FIELDS
    # ==========================================

    def clear_fields(self):

        for entry in [
            self.roll_entry,  self.name_entry,    self.age_entry,
            self.gender_entry, self.course_entry, self.email_entry,
            self.phone_entry,  self.address_entry
        ]:
            entry.delete(0, tk.END)