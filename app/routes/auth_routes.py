# =====================================================
# Auth Routes
# Replaces gui/start_window.py, gui/login_window.py,
# gui/register_window.py
#
# Handles the Start page, Admin Registration, Admin
# Login, and Logout. Session (Flask's signed cookie)
# replaces the Tkinter app's "which window is open" state.
# =====================================================

from functools import wraps

from flask import (
    Blueprint, render_template, request,
    redirect, url_for, session, flash
)

from app.database.db_connection import (
    get_connection,
    close_connection
)

from app.services.password_helper import hash_password, verify_password

from app.services.validations import (
    validate_required_fields,
    validate_username,
    validate_password
)

auth_bp = Blueprint("auth", __name__)


# =====================================================
# LOGIN REQUIRED DECORATOR
# Used by student_routes.py and history_routes.py to
# protect every page that used to live behind the
# Tkinter Dashboard (i.e. everything after login).
# =====================================================

def login_required(view_func):

    @wraps(view_func)
    def wrapped(*args, **kwargs):

        if "admin_id" not in session:
            flash("Please log in to continue.", "error")
            return redirect(url_for("auth.login"))

        return view_func(*args, **kwargs)

    return wrapped


# =====================================================
# START PAGE
# ("/") — same role as StartWindow: choose Login or Register
# =====================================================

@auth_bp.route("/")
def start():

    # IF ALREADY LOGGED IN, GO STRAIGHT TO DASHBOARD
    if "admin_id" in session:
        return redirect(url_for("student.dashboard"))

    return render_template("start.html")


# =====================================================
# REGISTER ADMIN
# =====================================================

@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "GET":
        return render_template("register.html")

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()

    # ======================================
    # STEP 1 — REQUIRED FIELDS CHECK
    # ======================================

    admin_data = {
        "Username": username,
        "Password": password,
    }

    missing_fields = validate_required_fields(admin_data)

    if missing_fields:
        if len(missing_fields) == 1:
            flash(f"Please enter your {missing_fields[0]}.", "error")
        else:
            flash("Please fill in all required fields.", "error")
        return render_template("register.html", username=username)

    # ======================================
    # STEP 2 — USERNAME FORMAT VALIDATION
    # ======================================

    username_error = validate_username(username)

    if username_error:
        flash(username_error, "error")
        return render_template("register.html", username=username)

    # ======================================
    # STEP 3 — PASSWORD FORMAT VALIDATION
    # ======================================

    password_error = validate_password(password)

    if password_error:
        flash(password_error, "error")
        return render_template("register.html", username=username)

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
            flash("Username Already Exists", "error")
            return render_template("register.html", username=username)

        # HASH THE PASSWORD BEFORE STORING
        hashed_password = hash_password(password)

        # INSERT NEW ADMIN RECORD
        cursor.execute(
            "INSERT INTO admins (username, password) VALUES (?, ?)",
            (username, hashed_password)
        )

        conn.commit()

        flash("Admin Registered Successfully. Please log in.", "success")

        # REDIRECT TO LOGIN AFTER SUCCESSFUL REGISTRATION
        return redirect(url_for("auth.login"))

    except Exception as error:

        flash(str(error), "error")
        return render_template("register.html", username=username)

    finally:

        close_connection(conn, cursor)


# =====================================================
# LOGIN
# =====================================================

@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()

    # ======================================
    # STEP 1 — REQUIRED FIELDS CHECK
    # ======================================

    login_data = {
        "Username": username,
        "Password": password,
    }

    missing_fields = validate_required_fields(login_data)

    if missing_fields:
        if len(missing_fields) == 1:
            flash(f"Please enter your {missing_fields[0]}.", "error")
        else:
            flash("Please fill in all required fields.", "error")
        return render_template("login.html", username=username)

    # ======================================
    # STEP 2 — USERNAME FORMAT VALIDATION
    # ======================================

    username_error = validate_username(username)

    if username_error:
        flash(username_error, "error")
        return render_template("login.html", username=username)

    # ======================================
    # STEP 3 — PASSWORD FORMAT VALIDATION
    # ======================================

    password_error = validate_password(password)

    if password_error:
        flash(password_error, "error")
        return render_template("login.html", username=username)

    # ======================================
    # STEP 4 — DATABASE AUTHENTICATION
    # ======================================

    conn   = None
    cursor = None

    try:

        conn, cursor = get_connection()

        # FETCH STORED HASH FOR THIS USERNAME
        cursor.execute(
            "SELECT admin_id, password FROM admins WHERE username = ?",
            (username,)
        )

        admin = cursor.fetchone()

        # USERNAME NOT FOUND
        if admin is None:

            # CHECK WHETHER ANY ADMIN EXISTS
            cursor.execute("SELECT COUNT(*) AS total FROM admins")
            admin_count = cursor.fetchone()["total"]

            if admin_count == 0:
                flash("No admin account exists. Please register an admin account first.", "info")
            else:
                flash("Username does not exist.", "error")

            return render_template("login.html", username=username)

        stored_password = admin["password"]

        # VERIFY ENTERED PASSWORD AGAINST STORED HASH
        if verify_password(password, stored_password):

            # STORE LOGIN STATE IN THE SESSION
            session["admin_id"] = admin["admin_id"]
            session["username"] = username

            flash("Login Successful", "success")

            return redirect(url_for("student.dashboard"))

        else:

            flash("Invalid Password", "error")
            return render_template("login.html", username=username)

    except Exception as error:

        flash(str(error), "error")
        return render_template("login.html", username=username)

    finally:

        close_connection(conn, cursor)


# =====================================================
# LOGOUT
# =====================================================

@auth_bp.route("/logout")
def logout():

    session.clear()
    flash("You have been logged out.", "info")

    return redirect(url_for("auth.start"))