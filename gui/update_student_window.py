# =====================================================
# Update Student Window
# Search for a student then update one or all fields
# Every update is logged to the updated_students table
# DB logic is handled in utils/update_student_actions.py
# =====================================================

import tkinter as tk
from tkinter import messagebox

from database.db_connection import (
    get_connection,
    close_connection
)

from utils.validations import validate_roll_no

import utils.update_student_actions as actions

class UpdateStudentWindow:

    def __init__(self, root):

        self.window = tk.Toplevel(root)

        # ==========================================
        # WINDOW SETTINGS
        # ==========================================

        self.window.title("Update Student")
        self.window.geometry("520x690")
        self.window.resizable(False, True)
        
        self.window.focus_force()
        
        # STORES CURRENT STUDENT DATA FETCHED FROM DB
        self.old_data = None

        # STORES THE ROLL NUMBER OF FETCHED STUDENT
        self.roll_no  = None

        self.build_ui()

    # ==========================================
    # BUILD UI
    # ==========================================

    def build_ui(self):

        # ======== SCROLLABLE CANVAS SETUP ========

        # CANVAS + VERTICAL SCROLLBAR
        canvas    = tk.Canvas(self.window)
        scrollbar = tk.Scrollbar(self.window, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # INNER FRAME INSIDE CANVAS — all widgets go here
        self.inner = tk.Frame(canvas)
        canvas_window = canvas.create_window((0, 0), window=self.inner, anchor="n")

        # CENTER THE INNER FRAME HORIZONTALLY AS WINDOW RESIZES
        def on_canvas_resize(event):
            canvas.itemconfig(canvas_window, width=event.width)
        canvas.bind("<Configure>", on_canvas_resize)

        # UPDATE SCROLL REGION WHENEVER INNER FRAME SIZE CHANGES
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        self.inner.bind("<Configure>", on_frame_configure)

        # MOUSE WHEEL SCROLLING
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)

        # HEADING
        tk.Label(
            self.inner,
            text="Update Student",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        # ======== ROLL NUMBER SEARCH SECTION ========

        tk.Label(
            self.inner,
            text="Enter Roll Number:",
            font=("Arial", 11)
        ).pack()

        self.roll_entry = tk.Entry(
            self.inner,
            width=30,
            font=("Arial", 11)
        )
        self.roll_entry.pack(ipady=2)

        tk.Button(
            self.inner,
            text="Search Student",
            font=("Arial", 11),
            command=self.search_student
        ).pack(pady=8)

        # ======== STUDENT INFO DISPLAY ========

        # INFO LABEL — always packed here to lock position in layout
        # text is empty initially, fills when student is found
        self.info_label = tk.Label(
            self.inner,
            text="",
            fg="blue",
            font=("Arial", 11),
            justify="left",
            anchor="nw"
        )
        self.info_label.pack(fill="x", padx=20)

        # ======== EDITABLE INPUT FIELDS ========

        # Each field has a label + entry created via helper
        self.name_entry    = self.create_field("Name")
        self.age_entry     = self.create_field("Age")
        self.gender_entry  = self.create_field("Gender")
        self.course_entry  = self.create_field("Course")
        self.email_entry   = self.create_field("Email")
        self.phone_entry   = self.create_field("Phone")
        self.address_entry = self.create_field("Address")

        # ======== INDIVIDUAL UPDATE BUTTONS ========

        btn_cfg = {"font": ("Arial", 11), "width": 20}

        tk.Button(self.inner, text="Update Name",    command=self.update_name,    **btn_cfg).pack(pady=(15, 2))
        tk.Button(self.inner, text="Update Age",     command=self.update_age,     **btn_cfg).pack(pady=2)
        tk.Button(self.inner, text="Update Gender",  command=self.update_gender,  **btn_cfg).pack(pady=2)
        tk.Button(self.inner, text="Update Course",  command=self.update_course,  **btn_cfg).pack(pady=2)
        tk.Button(self.inner, text="Update Email",   command=self.update_email,   **btn_cfg).pack(pady=2)
        tk.Button(self.inner, text="Update Phone",   command=self.update_phone,   **btn_cfg).pack(pady=2)
        tk.Button(self.inner, text="Update Address", command=self.update_address, **btn_cfg).pack(pady=2)

        # UPDATE ALL BUTTON (green)
        tk.Button(
            self.inner,
            text="Update All",
            font=("Arial", 11),
            width=20,
            bg="green",
            fg="white",
            command=self.update_all
        ).pack(pady=8)

        # UTILITY BUTTONS
        tk.Button(self.inner, text="Clear", font=("Arial", 11), width=20, command=self.clear_fields).pack(pady=2)
        # tk.Button(self.inner, text="Exit",  font=("Arial", 11), width=20, command=self.window.destroy).pack(pady=5)

    # ==========================================
    # HELPER — CREATE LABEL + ENTRY FIELD
    # ==========================================

    def create_field(self, label):
        """Creates a label + entry pair and returns the entry widget."""

        tk.Label(
            self.inner,
            text=label,
            font=("Arial", 11)
        ).pack()

        entry = tk.Entry(
            self.inner,
            width=30,
            font=("Arial", 11)
        )
        entry.pack(ipady=2)

        return entry

    # ==========================================
    # SEARCH STUDENT BY ROLL NUMBER
    # ==========================================

    def search_student(self):

        roll = self.roll_entry.get().strip()

        # VALIDATE ROLL NUMBER FORMAT
        roll_error = validate_roll_no(roll)

        if roll_error:
            messagebox.showerror(
                "Invalid Roll Number",
                roll_error,
                parent=self.window      # KEEPS WINDOW IN FRONT
            )
            return

        self.roll_no = int(roll)

        conn   = None
        cursor = None

        try:

            conn, cursor = get_connection()

            cursor.execute(
                "SELECT * FROM students WHERE roll_no = ?",
                (self.roll_no,)
            )

            self.old_data = cursor.fetchone()

            if not self.old_data:
                messagebox.showerror(
                    "Not Found",
                    "Student Not Found",
                    parent=self.window      # KEEPS WINDOW IN FRONT
                )
                return

            # DISPLAY STUDENT DATA IN LABEL
            self.display_student()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e),
                parent=self.window          # KEEPS WINDOW IN FRONT
            )

        finally:

            close_connection(conn, cursor)

    # ==========================================
    # DISPLAY FETCHED STUDENT DATA IN LABEL
    # ==========================================

    def display_student(self):

        self.info_label.config(
            text=(
                f"  Name    : {self.old_data['full_name']}\n"
                f"  Age     : {self.old_data['age']}\n"
                f"  Gender  : {self.old_data['gender']}\n"
                f"  Course  : {self.old_data['course']}\n"
                f"  Email   : {self.old_data['email']}\n"
                f"  Phone   : {self.old_data['phone']}\n"
                f"  Address : {self.old_data['address']}"
            )
        )
    
    # ==========================================
    # CLEAR ONLY ENTRY FIELDS (after update)
    # ==========================================

    def clear_entries(self):

        for entry in [
            self.name_entry,   self.age_entry,
            self.gender_entry, self.course_entry,
            self.email_entry,  self.phone_entry,
            self.address_entry
        ]:
            entry.delete(0, tk.END)

    # ==========================================
    # REFRESH — Reload student data after update
    # ==========================================

    def refresh(self):

        conn = None; cursor = None

        try:
            conn, cursor = get_connection()

            cursor.execute("SELECT * FROM students WHERE roll_no = ?", (self.roll_no,))

            self.old_data = cursor.fetchone()

            self.display_student()

            # CLEAR ENTRY FIELDS AFTER SUCCESSFUL UPDATE
            self.clear_entries()
        
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self.window)
        
        finally:
            close_connection(conn, cursor)

    # ==========================================
    # CLEAR ALL FIELDS AND RESET STATE
    # ==========================================

    def clear_fields(self):

        # CLEAR ROLL NUMBER ENTRY
        self.roll_entry.delete(0, tk.END)

        # CLEAR ALL FIELD ENTRIES
        self.clear_entries()

        # HIDE INFO LABEL AND RESET STATE
        self.info_label.pack_forget()
        self.info_label.config(text="")
        self.old_data = None
        self.roll_no  = None
    
    # ==========================================
    # UPDATE HANDLERS — delegate to actions module
    # ==========================================
 
    def update_name(self):

        if not self.old_data:
            messagebox.showerror(
                "Error",
                "Please search a student first.",
                parent=self.window
            )
            return
        
        actions.update_name(
            self.window, self.old_data, self.roll_no,
            self.name_entry.get().strip(),
            self.refresh
        )
    
    def update_age(self):
        
        if not self.old_data:
            messagebox.showerror(
                "Error",
                "Please search a student first.",
                parent=self.window
            )
            return
        
        actions.update_age(
            self.window, self.old_data, self.roll_no,
            self.age_entry.get().strip(),
            self.refresh
        )
 
    def update_gender(self):
        
        if not self.old_data:
            messagebox.showerror(
                "Error",
                "Please search a student first.",
                parent=self.window
            )
            return
        
        actions.update_gender(
            self.window, self.old_data, self.roll_no,
            self.gender_entry.get().strip(),
            self.refresh
        )
 
    def update_course(self):
        
        if not self.old_data:
            messagebox.showerror(
                "Error",
                "Please search a student first.",
                 parent=self.window
            )
            return
        
        actions.update_course(
            self.window, self.old_data, self.roll_no,
            self.course_entry.get().strip(),
            self.refresh
        )
 
    def update_email(self):
        
        if not self.old_data:
            messagebox.showerror(
                "Error",
                "Please search a student first.",
                parent=self.window
            )
            return
        
        actions.update_email(
            self.window, self.old_data, self.roll_no,
            self.email_entry.get().strip(),
            self.refresh
        )
 
    def update_phone(self):
        if not self.old_data:

            messagebox.showerror(
                "Error",
                "Please search a student first.",
                parent=self.window
            )
            return
        
        actions.update_phone(
            self.window, self.old_data, self.roll_no,
            self.phone_entry.get().strip(),
            self.refresh
        )
 
    def update_address(self):
        if not self.old_data:

            messagebox.showerror(
                "Error",
                "Please search a student first.",
                parent=self.window
            )
            return
        
        actions.update_address(
            self.window, self.old_data, self.roll_no,
            self.address_entry.get().strip(),
            self.refresh
        )
 
    def update_all(self):

        if not self.old_data:
            messagebox.showerror(
                "Error",
                "Please search a student first.",
                parent=self.window
            )
            return
        
        actions.update_all(
            self.window, self.old_data, self.roll_no,
            {
                "new_name":    self.name_entry.get().strip(),
                "age":         self.age_entry.get().strip(),
                "new_gender":  self.gender_entry.get().strip(),
                "new_course":  self.course_entry.get().strip(),
                "new_email":   self.email_entry.get().strip(),
                "new_phone":   self.phone_entry.get().strip(),
                "new_address": self.address_entry.get().strip(),
            },
            self.refresh
        )