# =====================================================
# Flask App Factory
# Replaces main.py's role of wiring everything together
# (tk.Tk() root window + StartWindow + mainloop, in the
#  Tkinter version) with create_app() + a dev server.
# =====================================================

from flask import Flask

from app.config import SECRET_KEY

# DATABASE INITIALIZATION
from app.database.db_creation import create_tables


def create_app():

    app = Flask(__name__)

    app.config["SECRET_KEY"] = SECRET_KEY

    # ==========================================
    # CREATE ALL DATABASE TABLES (if not already created)
    # Same call as main.py made before opening the GUI
    # ==========================================

    create_tables()

    # ==========================================
    # REGISTER BLUEPRINTS
    # Each blueprint groups the routes that replaced
    # one area of the old gui/ package
    # ==========================================

    from app.routes.auth_routes import auth_bp
    from app.routes.student_routes import student_bp
    from app.routes.history_routes import history_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(history_bp)

    # ==========================================
    # PREVENT BROWSER BACK/FORWARD CACHE
    # Without this, clicking the browser's Back
    # button after Logout can redisplay a cached
    # copy of the Dashboard (or any protected page)
    # straight from browser memory, without ever
    # asking the server again — which skips the
    # login_required check entirely. These headers
    # force the browser to always re-request the
    # page from Flask, so a logged-out session
    # correctly bounces back to the Login page.
    # ==========================================
 
    @app.after_request
    def add_no_cache_headers(response):
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

    return app