# =====================================================
# Allows a new admin to create an account
# Password is hashed before storing in the database
# =====================================================

import tkinter as tk
from tkinter import messagebox

from database.db_connection import (
    get_connection,
    close_connection
)

from utils.password_helper import hash_password

from utils.validations import (
    validate_required_fields,
    validate_username,
    validate_password
)


class RegisterWindow:

    def __init__(self, root):

        self.root = root

        # ==========================================
        # WINDOW SETTINGS
        # ==========================================

        self.root.title("Student Management System")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        # ==========================================
        # HEADING
        # ==========================================

        tk.Label(
            root,
            text="Register Admin",
            font=("Arial", 16, "bold")
        ).pack(pady=15)

        # ==========================================
        # USERNAME FIELD
        # ==========================================

        tk.Label(
            root,
            text="Username",
            font=("Arial", 11)
        ).pack()

        self.username_entry = tk.Entry(
            root,
            width=30,
            font=("Arial", 11)
        )

        self.username_entry.pack(pady=10, ipady=2)

        # ==========================================
        # PASSWORD FIELD WITH EYE TOGGLE
        # ==========================================

        tk.Label(
            root,
            text="Password",
            font=("Arial", 11)
        ).pack()

        # FRAME TO HOLD ENTRY + EYE BUTTON SIDE BY SIDE
        password_frame = tk.Frame(root)
        password_frame.pack(pady=5)

        self.password_entry = tk.Entry(
            password_frame,
            width=30,
            font=("Arial", 11),
            show="*"           # HIDE PASSWORD BY DEFAULT
        )

        self.password_entry.pack(side=tk.LEFT, ipady=2)

        # EYE BUTTON — hidden until user focuses on password field
        self.eye_btn = tk.Button(
            password_frame,
            text="👁",
            width=3,
            command=self.toggle_password
        )

        self.eye_btn.pack(side=tk.LEFT, padx=5)
        self.eye_btn.pack_forget()     # HIDE INITIALLY

        # SHOW EYE BUTTON WHEN PASSWORD FIELD IS ACTIVE
        self.password_entry.bind("<FocusIn>",   self.show_eye_button)
        self.password_entry.bind("<KeyRelease>", self.show_eye_button)

        # HIDE EYE BUTTON WHEN FOCUS LEAVES PASSWORD FIELD
        self.password_entry.bind("<FocusOut>",  self.hide_eye_button)

        # ==========================================
        # REGISTER BUTTON
        # ==========================================

        tk.Button(
            root,
            text="Register",
            font=("Arial", 11),
            width=13,
            command=self.register_admin
        ).pack(pady=15)

        # ==========================================
        # WINDOW-WIDE CLICK HANDLER
        # ==========================================
 
        self.root.bind("<Button-1>", self.clear_focus_if_needed)
    
    # ==========================================
    # CLEAR FOCUS IF NEEDED
    # ==========================================
 
    def clear_focus_if_needed(self, event):
 
        clicked_widget = event.widget
 
        if clicked_widget not in (self.password_entry, self.eye_btn):
            clicked_widget.focus_set()

    # ==========================================
    # SHOW EYE BUTTON
    # Called when user focuses or types in password field
    # ==========================================

    def show_eye_button(self, event=None):

        self.eye_btn.pack(side=tk.LEFT, padx=5)

    # ==========================================
    # HIDE EYE BUTTON
    # Called when focus leaves the password field
    # Also resets password to hidden (show="*")
    # ==========================================

    def hide_eye_button(self, event=None):

        # DON'T HIDE IF EYE BUTTON ITSELF HAS FOCUS
        if self.root.focus_get() != self.eye_btn:

            self.eye_btn.pack_forget()

            # RESET TO HIDDEN STATE
            self.password_entry.config(show="*")
            self.eye_btn.config(text="👁")

    # ==========================================
    # TOGGLE PASSWORD VISIBILITY
    # ==========================================

    def toggle_password(self):

        if self.password_entry.cget("show") == "*":

            # SHOW PASSWORD
            self.password_entry.config(show="")
            self.eye_btn.config(text="⌧")

        else:

            # HIDE PASSWORD
            self.password_entry.config(show="*")
            self.eye_btn.config(text="👁")

    # ==========================================
    # REGISTER ADMIN
    # ==========================================

    def register_admin(self):

        # GET INPUT VALUES
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        # ======================================
        # STEP 1 — REQUIRED FIELDS CHECK
        # ======================================

        admin_data = {
            "Username": username,
            "Password": password,
        }

        missing_fields = validate_required_fields(admin_data)

        if missing_fields:
            messagebox.showerror(
                "Required Fields",
                "Please fill the following fields:\n\n"
                + "\n".join(missing_fields)
            )
            return

        # ======================================
        # STEP 2 — USERNAME FORMAT VALIDATION
        # ======================================

        username_error = validate_username(username)

        if username_error:
            messagebox.showerror("Invalid Username", username_error)
            return

        # ======================================
        # STEP 3 — PASSWORD FORMAT VALIDATION
        # ======================================

        password_error = validate_password(password)

        if password_error:
            messagebox.showerror("Invalid Password", password_error)
            return

        # ======================================
        # STEP 4 — DATABASE OPERATIONS
        # ======================================

        conn   = None
        cursor = None

        try:

            conn, cursor = get_connection()

            # CHECK IF USERNAME ALREADY EXISTS
            cursor.execute(
                "SELECT 1 FROM admins WHERE username = ?",
                (username,)
            )

            if cursor.fetchone():
                messagebox.showerror(
                    "Registration Failed",
                    "Username Already Exists"
                )
                return

            # HASH THE PASSWORD BEFORE STORING
            hashed_password = hash_password(password)

            # INSERT NEW ADMIN RECORD
            cursor.execute(
                "INSERT INTO admins (username, password) VALUES (?, ?)",
                (username, hashed_password)
            )

            conn.commit()

            messagebox.showinfo(
                "Registration Successful",
                "Admin Registered Successfully"
            )

            # REDIRECT TO LOGIN AFTER SUCCESSFUL REGISTRATION
            self.open_login()

        except Exception as error:

            messagebox.showerror("Database Error", str(error))

        finally:

            close_connection(conn, cursor)

    # ==========================================
    # OPEN LOGIN WINDOW
    # ==========================================

    def open_login(self):

        from gui.login_window import LoginWindow

        self.clear_window()
        LoginWindow(self.root)

    # ==========================================
    # CLEAR WINDOW
    # Destroys all widgets before switching screen
    # ==========================================

    def clear_window(self):

        for widget in self.root.winfo_children():
            widget.destroy()