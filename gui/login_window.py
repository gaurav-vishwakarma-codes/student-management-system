# =====================================================
# Allows existing admins to log into the system
# Validates credentials against the admins table
# =====================================================

import tkinter as tk
from tkinter import messagebox

from database.db_connection import (
    get_connection,
    close_connection
)

from utils.password_helper import verify_password

from utils.validations import (
    validate_required_fields,
    validate_username,
    validate_password
)

from gui.dashboard import Dashboard


class LoginWindow:

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
            text="Admin Login",
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
        # PASSWORD FIELD
        # ==========================================

        tk.Label(
            root,
            text="Password",
            font=("Arial", 11)
        ).pack()

        self.password_entry = tk.Entry(
            root,
            width=30,
            font=("Arial", 11),
            show="*"           # HIDE PASSWORD CHARACTERS
        )

        self.password_entry.pack(pady=10, ipady=2)

        # ==========================================
        # LOGIN BUTTON
        # ==========================================

        tk.Button(
            root,
            text="Login",
            font=("Arial", 11),
            width=13,
            command=self.login
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
 
        if clicked_widget not in (self.username_entry , self.password_entry):
            clicked_widget.focus_set()

    # ==========================================
    # LOGIN FUNCTION
    # ==========================================

    def login(self):

        # GET INPUT VALUES
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        # ======================================
        # STEP 1 — REQUIRED FIELDS CHECK
        # ======================================

        login_data = {
            "Username": username,
            "Password": password,
        }

        missing_fields = validate_required_fields(login_data)

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
            messagebox.showerror("Error", username_error)
            return

        # ======================================
        # STEP 3 — PASSWORD FORMAT VALIDATION
        # ======================================

        password_error = validate_password(password)

        if password_error:
            messagebox.showerror("Error", password_error)
            return

        # ======================================
        # STEP 4 — DATABASE AUTHENTICATION
        # ======================================

        conn   = None
        cursor = None

        try:

            conn, cursor = get_connection()

            # FETCH STORED HASH FOR THIS USERNAME
            cursor.execute(
                "SELECT password FROM admins WHERE username = ?",
                (username,)
            )

            admin = cursor.fetchone()

            # USERNAME NOT FOUND
            if admin is None:
                
                # CHECK WHETHER ANY ADMIN EXISTS
                cursor.execute("SELECT COUNT(*) AS total FROM admins")
                admin_count = cursor.fetchone()["total"]

                if admin_count == 0:

                    messagebox.showinfo(
                        "No Admin Found",
                        "No admin account exists.\n\n"
                        "Please register an admin account first."
                    )

                else:

                    messagebox.showerror(
                        "Login Failed",
                        "Username does not exist."
                    )

                return

            stored_password = admin["password"]

            # VERIFY ENTERED PASSWORD AGAINST STORED HASH
            if verify_password(password, stored_password):

                messagebox.showinfo("Success", "Login Successful")

                # OPEN DASHBOARD ON SUCCESS
                self.open_dashboard()

            else:

                messagebox.showerror("Error", "Invalid Password")

        except Exception as error:

            messagebox.showerror("Error", str(error))

        finally:

            close_connection(conn, cursor)

    # ==========================================
    # OPEN DASHBOARD
    # Destroys login window and opens a new root for dashboard
    # ==========================================

    def open_dashboard(self):

        # CLOSE THE LOGIN WINDOW
        self.root.destroy()

        # CREATE A FRESH ROOT WINDOW FOR DASHBOARD
        dashboard_root = tk.Tk()

        Dashboard(dashboard_root)

        dashboard_root.focus_force()

        dashboard_root.mainloop()