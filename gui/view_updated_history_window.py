# =====================================================
# Displays full history of all student field updates
# Shows old values, which field changed, and new value
# DB work is delegated to utils/history_service.py
# =====================================================

import tkinter as tk
from tkinter import ttk, messagebox

import utils.history_service as history_service

class UpdatedHistoryWindow:

    def __init__(self, root):

        self.window = tk.Toplevel(root)

        # ==========================================
        # WINDOW SETTINGS
        # ==========================================

        self.window.title("Updated Students History")
        self.window.geometry("1200x500")

        self.window.focus_force()
        
        self.create_widgets()
        self.load_history()

    # ==========================================
    # CREATE WIDGETS
    # ==========================================

    def create_widgets(self):

        # HEADING
        tk.Label(
            self.window,
            text="Updated Students History",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        # TABLE COLUMNS
        columns = (
            "Update ID", "Roll No", "Old Name", "Old Age",
            "Old Gender", "Old Course", "Old Email", "Old Phone",
            "Old Address", "Updated Field", "New Value", "Updated At"
        )

        # TREEVIEW TABLE
        self.tree = ttk.Treeview(
            self.window,
            columns=columns,
            show="headings"
        )

        # SCROLLBARS
        vertical_scrollbar = ttk.Scrollbar(
            self.window,
            orient="vertical",
            command=self.tree.yview
        )

        horizontal_scrollbar = ttk.Scrollbar(
            self.window,
            orient="horizontal",
            command=self.tree.xview
        )

        self.tree.configure(
            yscrollcommand=vertical_scrollbar.set,
            xscrollcommand=horizontal_scrollbar.set
        )

        # SET COLUMN HEADINGS AND WIDTHS
        for column in columns:
            self.tree.heading(column, text=column)

            if column == "Old Address":
                self.tree.column(column, width=250, anchor="w")
            elif column == "Old Email":
                self.tree.column(column, width=220, anchor="center")
            else:
                self.tree.column(column, width=140, anchor="center")

        self.tree.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(10, 0)
        )
        horizontal_scrollbar.pack(fill="x")
        vertical_scrollbar.pack(side="right", fill="y")

    # ==========================================
    # LOAD UPDATED HISTORY FROM DATABASE
    # ==========================================

    def load_history(self):

        try:
            
            # FETCH ALL UPDATE RECORDS (NEWEST FIRST)
            records = history_service.get_updated_history()

            # CLEAR EXISTING ROWS BEFORE INSERTING NEW DATA
            for item in self.tree.get_children():
                self.tree.delete(item)

            # INSERT EACH RECORD AS A ROW
            for row in records:
                self.tree.insert("", tk.END, values=tuple(row))

        except Exception as error:

            messagebox.showerror(
                "Database Error",
                str(error),
                parent=self.window
            )
