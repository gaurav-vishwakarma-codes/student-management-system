# =====================================================
# Student Routes
# Replaces gui/dashboard.py, gui/add_student_window.py,
# gui/view_students_window.py, gui/search_student_window.py,
# gui/update_student_window.py, gui/delete_student_window.py
#
# All DB work is delegated to app/services/*.py, exactly
# as the Tkinter windows delegated to utils/*.py.
# =====================================================

from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash
)

import app.services.student_service as student_service
import app.services.update_student_actions as actions

from app.database.dummy_data import insert_dummy_students

from app.services.validations import (
    validate_required_fields,
    validate_roll_no,
    validate_name,
    validate_age,
    validate_gender,
    validate_course,
    validate_email,
    validate_phone,
    validate_address,
    validate_search_query
)

from app.routes.auth_routes import login_required

student_bp = Blueprint("student", __name__)


# =====================================================
# DASHBOARD
# Replaces gui/dashboard.py — the main menu
# =====================================================

@student_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


# =====================================================
# LOAD DUMMY DATA
# Replaces Dashboard.load_dummy_data()
# =====================================================

@student_bp.route("/dashboard/load-dummy", methods=["POST"])
@login_required
def load_dummy_data():

    success, inserted_count, skipped_count = insert_dummy_students()

    if not success:
        flash("Failed to insert dummy student records.", "error")
    elif inserted_count == 0:
        flash("All dummy students already exist — nothing new to add.", "info")
    else:
        message = f"{inserted_count} dummy student record(s) inserted successfully."
        if skipped_count:
            message += f" ({skipped_count} already existed and were skipped.)"
        flash(message, "success")

    return redirect(url_for("student.dashboard"))


# =====================================================
# ADD STUDENT
# Replaces gui/add_student_window.py
# =====================================================

@student_bp.route("/students/add", methods=["GET", "POST"])
@login_required
def add_student():

    if request.method == "GET":
        return render_template("add_student.html")

    roll_no   = request.form.get("roll_no", "").strip()
    full_name = request.form.get("full_name", "").strip()
    age       = request.form.get("age", "").strip()
    gender    = request.form.get("gender", "").strip()
    course    = request.form.get("course", "").strip()
    email     = request.form.get("email", "").strip()
    phone     = request.form.get("phone", "").strip()
    address   = request.form.get("address", "").strip()

    form_values = {
        "roll_no": roll_no, "full_name": full_name, "age": age,
        "gender": gender, "course": course, "email": email,
        "phone": phone, "address": address
    }

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
        flash("Please fill in all required fields.", "error")
        return render_template("add_student.html", **form_values)

    # ======================================
    # STEP 2 — INDIVIDUAL FIELD VALIDATIONS
    # ======================================

    validators = [
        validate_roll_no(roll_no),
        validate_name(full_name),
        validate_age(age),
        validate_gender(gender),
        validate_course(course),
        validate_email(email),
        validate_phone(phone),
        validate_address(address),
    ]

    for error in validators:
        if error:
            flash(error, "error")
            return render_template("add_student.html", **form_values)

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
        flash(message, "error")
        return render_template("add_student.html", **form_values)

    flash(message, "success")

    # FRESH FORM AFTER SUCCESS (Tkinter version cleared the fields too)
    return redirect(url_for("student.add_student"))


# =====================================================
# VIEW STUDENTS
# Replaces gui/view_students_window.py
# =====================================================

@student_bp.route("/students")
@login_required
def view_students():

    try:
        students = student_service.get_all_students()
    except Exception as error:
        flash(str(error), "error")
        students = []

    return render_template("view_students.html", students=students)


# =====================================================
# SEARCH STUDENT
# Replaces gui/search_student_window.py — extended to
# search by Name, Course, Email, Phone, or Address too,
# not just Roll Number.
# =====================================================

@student_bp.route("/students/search")
@login_required
def search_student():

    search_by = request.args.get("search_by", "roll_no").strip()
    query     = request.args.get("query", "").strip()

    students = []
    searched = False

    if search_by not in student_service.SEARCHABLE_FIELDS:
        search_by = "roll_no"

    if query:

        searched = True

        # FIELD-AWARE VALIDATION — CATCHES INPUT THAT OBVIOUSLY
        # DOESN'T BELONG IN THE CHOSEN FIELD (E.G. "22" WHILE
        # SEARCHING BY FULL NAME) BEFORE EVEN QUERYING THE
        # DATABASE, SO THE PERSON GETS ONE CLEAR, SPECIFIC
        # MESSAGE INSTEAD OF A GENERIC "NO RESULTS"
        query_error = validate_search_query(search_by, query)

        if query_error:
            flash(query_error, "error")
            searched = False  # DON'T SHOW "NO RESULTS" ON A VALIDATION ERROR
        else:
            try:
                students = student_service.search_students(search_by, query)
            except Exception as error:
                flash(str(error), "error")
                searched = False

        if searched and not students:
            flash("No Student Found", "info")

    return render_template(
        "search_student.html",
        students=students,
        search_by=search_by,
        query=query,
        searched=searched
    )


# =====================================================
# UPDATE STUDENT — SEARCH + FORM
# Replaces gui/update_student_window.py
# =====================================================

@student_bp.route("/students/update")
@login_required
def update_student_search():

    roll_no = request.args.get("roll_no", "").strip()
    student = None

    if roll_no:

        roll_no_error = validate_roll_no(roll_no)

        if roll_no_error:
            flash(roll_no_error, "error")
        else:
            try:
                student = student_service.get_student_by_roll(int(roll_no))
                if student is None:
                    flash("Student Not Found", "error")
            except Exception as error:
                flash(str(error), "error")

    return render_template("update_student.html", student=student, roll_no=roll_no)


# =====================================================
# UPDATE — SINGLE FIELD
# Replaces the per-field buttons in update_student_window.py
# / utils/update_student_actions.py
# =====================================================

# MAPS THE FORM FIELD NAME -> (service function, old_data key, form input name)
_SINGLE_FIELD_MAP = {
    "name":    (actions.update_name,    "full_name", "new_name"),
    "age":     (actions.update_age,     "age",       "age"),
    "gender":  (actions.update_gender,  "gender",    "new_gender"),
    "course":  (actions.update_course,  "course",    "new_course"),
    "email":   (actions.update_email,   "email",     "new_email"),
    "phone":   (actions.update_phone,   "phone",     "new_phone"),
    "address": (actions.update_address, "address",   "new_address"),
}


@student_bp.route("/students/update/<int:roll_no>/<field>", methods=["POST"])
@login_required
def update_student_field(roll_no, field):

    if field not in _SINGLE_FIELD_MAP:
        flash("Unknown field.", "error")
        return redirect(url_for("student.update_student_search", roll_no=roll_no))

    old_data = student_service.get_student_by_roll(roll_no)

    if old_data is None:
        flash("Student Not Found", "error")
        return redirect(url_for("student.update_student_search"))

    update_func, _old_key, input_name = _SINGLE_FIELD_MAP[field]
    new_value = request.form.get(input_name, "").strip()

    success, message = update_func(old_data, roll_no, new_value)

    if success:
        flash(message, "success")
        return redirect(url_for("student.update_student_search", roll_no=roll_no))

    # ON FAILURE — RE-RENDER DIRECTLY (NOT A REDIRECT) SO THE
    # DROPDOWN STAYS ON THIS FIELD AND THE TYPED VALUE ISN'T LOST
    flash(message, "error")

    return render_template(
        "update_student.html",
        student=old_data,
        roll_no=str(roll_no),
        active_field=field,
        form_values={input_name: new_value}
    )


# =====================================================
# UPDATE — ALL FIELDS
# =====================================================

@student_bp.route("/students/update/<int:roll_no>/all", methods=["POST"])
@login_required
def update_student_all(roll_no):

    old_data = student_service.get_student_by_roll(roll_no)

    if old_data is None:
        flash("Student Not Found", "error")
        return redirect(url_for("student.update_student_search"))

    fields = {
        "new_name":    request.form.get("new_name", "").strip(),
        "age":         request.form.get("age", "").strip(),
        "new_gender":  request.form.get("new_gender", "").strip(),
        "new_course":  request.form.get("new_course", "").strip(),
        "new_email":   request.form.get("new_email", "").strip(),
        "new_phone":   request.form.get("new_phone", "").strip(),
        "new_address": request.form.get("new_address", "").strip(),
    }

    success, message = actions.update_all(old_data, roll_no, fields)

    if success:
        flash(message, "success")
        return redirect(url_for("student.update_student_search", roll_no=roll_no))

    # ON FAILURE — RE-RENDER DIRECTLY (NOT A REDIRECT) SO THE
    # "ALL FIELDS" SECTION STAYS OPEN AND NOTHING TYPED IS LOST
    flash(message, "error")

    return render_template(
        "update_student.html",
        student=old_data,
        roll_no=str(roll_no),
        active_field="all",
        form_values=fields
    )


# =====================================================
# DELETE STUDENT — SEARCH + DELETE
# Replaces gui/delete_student_window.py
# =====================================================

@student_bp.route("/students/delete")
@login_required
def delete_student_search():

    # ======================================
    # ONE UNIFIED SEARCH — same dropdown +
    # value pattern as the Search page, using
    # the same SEARCHABLE_FIELDS (Roll Number
    # included). Results always render as a
    # checkbox table below, whether the search
    # matches one student or many — so a plain
    # Roll Number lookup and a "find everyone
    # in MCom" lookup both work the same way.
    # ======================================

    search_by = request.args.get("search_by", "").strip()
    query     = request.args.get("query", "").strip()

    students = []
    searched = False

    if search_by and query:

        searched = True

        if search_by not in student_service.SEARCHABLE_FIELDS:
            flash("Please choose a valid field to search by.", "error")
            searched = False
        else:
            query_error = validate_search_query(search_by, query)
            if query_error:
                flash(query_error, "error")
                searched = False
            else:
                try:
                    students = student_service.search_students(search_by, query)
                    if not students:
                        flash("No matching students found.", "info")
                except Exception as error:
                    flash(str(error), "error")
                    searched = False

    try:
        total_students = student_service.count_students()
    except Exception:
        total_students = 0

    return render_template(
        "delete_student.html",
        students=students,
        search_by=search_by,
        query=query,
        searched=searched,
        total_students=total_students
    )


@student_bp.route("/students/delete-all", methods=["POST"])
@login_required
def delete_all_students():

    success, message, count = student_service.delete_all_students()

    flash(message, "success" if success else ("info" if count == 0 else "error"))

    return redirect(url_for("student.delete_student_search"))


@student_bp.route("/students/delete/bulk", methods=["POST"])
@login_required
def delete_students_bulk():

    # PRESERVE THE SEARCH CRITERIA ON REDIRECT SO THE
    # RESULTS TABLE REAPPEARS INSTEAD OF RESETTING BLANK
    search_by = request.form.get("search_by", "").strip()
    query     = request.form.get("query", "").strip()

    selected = request.form.getlist("roll_no")

    if not selected:
        flash("Please select at least one student to delete.", "error")
        return redirect(url_for(
            "student.delete_student_search",
            search_by=search_by,
            query=query
        ))

    roll_nos = [int(r) for r in selected]

    success, message, count = student_service.bulk_delete_students(roll_nos)

    flash(message, "success" if success else ("info" if count == 0 else "error"))

    return redirect(url_for(
        "student.delete_student_search",
        search_by=search_by,
        query=query
    ))