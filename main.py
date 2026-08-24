# =====================================================
# Student Management System (Flask + SQLite)
# Main Entry Point — execution starts here
# =====================================================

from app import create_app

app = create_app()

if __name__ == "__main__":

    # DEBUG=TRUE GIVES AUTO-RELOAD + DETAILED ERROR PAGES DURING DEVELOPMENT
    # TURN THIS OFF (debug=False) BEFORE DEPLOYING ANYWHERE PUBLIC
    app.run(debug=True)