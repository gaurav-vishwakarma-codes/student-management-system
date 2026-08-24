# =====================================================
# History Routes
# Replaces gui/view_updated_history_window.py and
# gui/view_deleted_history_window.py
#
# The Tkinter version supported Ctrl+A / Ctrl+Click
# multi-select restore in a Treeview. The web version
# gets the same result with checkboxes in an HTML table
# and a single "Restore Selected" submit button.
# =====================================================

from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash
)

import app.services.history_service as history_service

from app.routes.auth_routes import login_required

history_bp = Blueprint("history", __name__)


# =====================================================
# UPDATED STUDENTS HISTORY
# =====================================================

@history_bp.route("/history/updated")
@login_required
def updated_history():

    try:
        records = history_service.get_updated_history()
    except Exception as error:
        flash(str(error), "error")
        records = []

    return render_template("updated_history.html", records=records)


# =====================================================
# DELETED STUDENTS HISTORY
# =====================================================

@history_bp.route("/history/deleted")
@login_required
def deleted_history():

    # PRESERVED FROM A PRIOR RESTORE/PERMANENT-DELETE SUBMIT
    # (see the redirects below) SO THE FILTER DOESN'T RESET
    # TO BLANK AFTER THE PAGE RELOADS
    filter_query = request.args.get("filter_query", "").strip()
    filter_field = request.args.get("filter_field", "").strip()

    try:
        records = history_service.get_deleted_history()
    except Exception as error:
        flash(str(error), "error")
        records = []

    return render_template(
        "deleted_history.html",
        records=records,
        filter_query=filter_query,
        filter_field=filter_field
    )


# =====================================================
# RESTORE SELECTED (SINGLE OR MULTI-SELECT)
# =====================================================

@history_bp.route("/history/deleted/restore", methods=["POST"])
@login_required
def restore_students():

    # THE FILTER BOX LIVES INSIDE THE FORM, SO ITS CURRENT
    # TEXT TRAVELS ALONG WITH THIS SUBMIT — WE PASS IT BACK
    # ON REDIRECT SO THE PAGE RELOADS WITH THE SAME FILTER
    # STILL APPLIED, INSTEAD OF RESETTING TO BLANK.
    filter_query = request.form.get("filter_query", "").strip()
    filter_field = request.form.get("filter_field", "").strip()

    # CHECKBOXES ALL SHARE THE NAME "roll_no"
    selected = request.form.getlist("roll_no")

    if not selected:
        flash("Please select at least one student to restore.", "error")
        return redirect(url_for("history.deleted_history", filter_query=filter_query, filter_field=filter_field))

    roll_nos = [int(r) for r in selected]

    try:

        restored, already_active, not_found = history_service.restore_students(roll_nos)

        # BUILD A CLEAN, READABLE RESULT MESSAGE
        lines = []

        if restored > 0:
            lines.append(f"{restored} student(s) restored successfully.")

        if already_active:
            lines.append(f"{len(already_active)} already active (skipped).")

        if not_found:
            lines.append(f"{len(not_found)} not found (may have been permanently deleted).")

        if restored == 0 and not already_active and not not_found:
            lines.append("No students were restored.")

        flash(" ".join(lines), "success" if restored else "info")

    except Exception as error:

        flash(str(error), "error")

    return redirect(url_for("history.deleted_history", filter_query=filter_query, filter_field=filter_field))


# =====================================================
# PERMANENTLY DELETE SELECTED (SINGLE OR MULTI-SELECT)
# Unlike Restore, this is IRREVERSIBLE — the record is
# removed from deleted_students entirely, with nowhere
# left to recover it from afterwards.
# =====================================================

@history_bp.route("/history/deleted/permanent-delete", methods=["POST"])
@login_required
def permanently_delete_students():

    # SAME REASONING AS restore_students() ABOVE — CARRY THE
    # TYPED FILTER TEXT THROUGH THE REDIRECT SO IT DOESN'T
    # RESET TO BLANK AFTER THIS BUTTON IS CLICKED.
    filter_query = request.form.get("filter_query", "").strip()
    filter_field = request.form.get("filter_field", "").strip()

    # SAME CHECKBOXES AS THE RESTORE FORM, SHARED VIA
    # THE BUTTON'S formaction (see deleted_history.html)
    selected = request.form.getlist("roll_no")

    if not selected:
        flash("Please select at least one student to permanently delete.", "error")
        return redirect(url_for("history.deleted_history", filter_query=filter_query, filter_field=filter_field))

    roll_nos = [int(r) for r in selected]

    try:

        deleted_count = history_service.permanently_delete_students(roll_nos)

        if deleted_count > 0:
            flash(f"{deleted_count} student(s) permanently deleted.", "success")
        else:
            flash("No matching students found to delete.", "info")

    except Exception as error:

        flash(str(error), "error")

    return redirect(url_for("history.deleted_history", filter_query=filter_query, filter_field=filter_field))