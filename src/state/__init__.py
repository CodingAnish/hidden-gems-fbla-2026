"""
Application state — single source of truth for user and UI preferences.
Enables consistent state across desktop and web. FBLA 2026.
"""
from .app_state import get_state, set_user, get_user, clear_user

__all__ = ["get_state", "set_user", "get_user", "clear_user"]
