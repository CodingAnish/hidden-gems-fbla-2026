"""
Hidden Gems — Entry point.
FBLA 2026 | Byte-Sized Business Boost
Standalone desktop app: email login with verification, SQLite storage.
"""
import sys
import os

# Ensure project root is on path and current directory so config.py and DB are found
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
os.chdir(ROOT)

from src.database.db import init_db
from src.ui.theme import setup_theme, apply_window_bg
from src.ui.login_window import show_login
from src.ui.main_menu import show_main_menu
from src.database import seed


def main():
    setup_theme()
    init_db()
    seed.ensure_seed_data()
    show_login(on_login_success=lambda user: show_main_menu(user))


if __name__ == "__main__":
    main()
