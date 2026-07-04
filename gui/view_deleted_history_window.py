# =====================================================
# Displays full history of all soft-deleted students
# Supports single-select/multi-select restore (Ctrl+A, Ctrl+Click)
# DB work is delegated to utils/history_service.py
# =====================================================

import tkinter as tk
from tkinter import ttk, messagebox

import utils.history_service as history_service


class DeletedHistoryWindow:

    def __init__(self, root):

        self.window = tk.Toplevel(root)

        # ==========================================
        # WINDOW SETTINGS
        # ==========================================

        self.window.title("Deleted Students History")
        self.window.geometry("1200x560")

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
            text="Deleted Students History",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        # TABLE COLUMNS
        columns = (
            "Delete ID", "Roll No", "Full Name", "Age",
            "Gender", "Course", "Email", "Phone", "Address", "Deleted At"
        )

        # TREEVIEW — extended mode allows Ctrl+Click, Shift+Click, Ctrl+A
        self.tree = ttk.Treeview(
            self.window,
            columns=columns,
            show="headings",
            selectmode="extended"
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

            if column == "Address":
                self.tree.column(column, width=250, anchor="w")
            elif column == "Email":
                self.tree.column(column, width=220, anchor="center")
            else:
                self.tree.column(column, width=140, anchor="center")

        self.tree.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(10, 0)
        )

        vertical_scrollbar.pack(side="right", fill="y")
        horizontal_scrollbar.pack(fill="x")

        # CTRL+A — SELECT ALL ROWS
        self.tree.bind("<Control-a>", self.select_all)

        # CLICK ON EMPTY AREA — DESELECT ALL
        self.tree.bind("<Button-1>", self.deselect_on_empty_click)

        # SELECTION CHANGE — UPDATE RESTORE BUTTON LABEL
        self.tree.bind("<<TreeviewSelect>>", self.update_restore_btn_label)

        # BUTTONS FRAME — holds Restore and Refresh side by side
        btn_frame = tk.Frame(self.window)
        btn_frame.pack(pady=10)

        # RESTORE BUTTON — disabled until data loads
        # Label updates dynamically based on how many rows are selected
        self.restore_btn = tk.Button(
            btn_frame,
            text="Restore Selected Student",
            font=("Arial", 11),
            state="disabled",
            command=self.restore_student
        )
        self.restore_btn.pack(side="left", padx=10)

        # REFRESH BUTTON — always enabled
        tk.Button(
            btn_frame,
            text="Refresh",
            font=("Arial", 11),
            command=self.load_history
        ).pack(side="left", padx=10)

    # ==========================================
    # UPDATE RESTORE BUTTON LABEL
    # Called whenever the Treeview selection changes
    # ==========================================

    def update_restore_btn_label(self, event=None):

        count = len(self.tree.selection())

        if count == 0:
            label = "Restore Selected Student"
        elif count == 1:
            label = "Restore Selected Student"
        else:
            label = f"Restore {count} Selected Students"

        self.restore_btn.config(text=label)

    # ==========================================
    # SELECT ALL ROWS (Ctrl+A)
    # ==========================================

    def select_all(self, event=None):

        self.tree.selection_set(self.tree.get_children())
        return "break"     # PREVENT DEFAULT BEHAVIOUR

    # ==========================================
    # DESELECT WHEN CLICKING EMPTY AREA
    # ==========================================

    def deselect_on_empty_click(self, event):

        # identify_row returns "" if click is not on a row
        if not self.tree.identify_row(event.y):
            self.tree.selection_remove(self.tree.selection())

    # ==========================================
    # LOAD DELETED HISTORY FROM DATABASE
    # ==========================================

    def load_history(self):

        try:

            records = history_service.get_deleted_history()
 
            # CLEAR EXISTING ROWS
            for item in self.tree.get_children():
                self.tree.delete(item)

            # INSERT EACH RECORD AS A ROW
            for row in records:
                self.tree.insert("", tk.END, values=tuple(row))

            # ENABLE RESTORE BUTTON ONLY IF RECORDS EXIST
            self.restore_btn.config(state="normal" if records else "disabled")
        
        except Exception as error:

            messagebox.showerror(
                "Database Error",
                str(error),
                parent=self.window
            )
    
    # ==========================================
    # RESTORE SELECTED STUDENT(S)
    # Supports single and multi-select restore
    # ==========================================

    def restore_student(self):

        # GET ALL SELECTED ROWS
        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning(
                "Selection Required",
                "Please select at least one student to restore.",
                parent=self.window
            )
            return

        # COLLECT ALL ROLL NUMBERS FROM SELECTED ROWS
        roll_nos = [self.tree.item(row)["values"][1] for row in selected]

        count = len(roll_nos)

        # CONFIRM MESSAGE — singular or plural
        if count == 1:
            msg = f"Restore Roll No {roll_nos[0]}?"
        else:
            msg = f"Restore {count} selected students?"

        confirm = messagebox.askyesno(
            "Confirm Restore",
            msg,
            parent=self.window
        )

        if not confirm:
            return


        try:

            restored, skipped = history_service.restore_students(roll_nos)
            
            # BUILD A CLEAN, READABLE RESULT MESSAGE
            lines = []

            if restored > 0:
                lines.append(f"✔  {restored} student(s) restored successfully.")

            if skipped:
                lines.append(f"✘  {len(skipped)} already active (skipped).")

            if restored == 0 and not skipped:
                lines.append("No students were restored.")

            messagebox.showinfo("Restore Complete", "\n".join(lines), parent=self.window)

            # REFRESH TABLE AND TOGGLE BUTTON STATE
            self.load_history()

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error),
                parent=self.window
            )