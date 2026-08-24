# =====================================================
# App Config
# Central place for app-wide constants
# =====================================================

import os

# NAME OF THE SQLITE DATABASE FILE (auto-created on first run)
DB_NAME = "student.db"

# SECRET KEY — required by Flask for session cookies + flash messages
# In production, set this via an environment variable instead.
SECRET_KEY = os.environ.get("SMS_SECRET_KEY", "dev-secret-key-change-me")