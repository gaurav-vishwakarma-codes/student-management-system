# =====================================================
# Start Window
# First screen shown when the application launches
# Gives the user the option to Login or Register
# =====================================================

import tkinter as tk

from gui.login_window    import LoginWindow
from gui.register_window import RegisterWindow


class StartWindow:

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
            text="Student Management System",
            font=("Arial", 16, "bold")
        ).pack(pady=30)

        # ==========================================
        # LOGIN SECTION
        # ==========================================

        tk.Label(
            root,
            text="Already have an account?",
            font=("Arial", 11)
        ).pack(pady=3)

        tk.Button(
            root,
            text="Login",
            width=15,
            font=("Arial", 11),
            command=self.open_login
        ).pack()

        # ==========================================
        # REGISTER SECTION
        # ==========================================

        tk.Label(
            root,
            text="New admin?",
            font=("Arial", 11)
        ).pack(pady=(20, 3))

        tk.Button(
            root,
            text="Register",
            width=15,
            font=("Arial", 11),
            command=self.open_register
        ).pack()

    # ==========================================
    # CLEAR WINDOW
    # Destroys all widgets before switching screen
    # ==========================================

    def clear_window(self):

        for widget in self.root.winfo_children():
            widget.destroy()

    # ==========================================
    # OPEN LOGIN WINDOW
    # ==========================================

    def open_login(self):

        self.clear_window()
        LoginWindow(self.root)

    # ==========================================
    # OPEN REGISTER WINDOW
    # ==========================================

    def open_register(self):

        self.clear_window()
        RegisterWindow(self.root)