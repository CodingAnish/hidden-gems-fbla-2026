"""
Centralized application state for Hidden Gems.
Supports desktop (in-memory) and web (session); keeps logic consistent.
FBLA 2026.
"""

_state = {"user": None, "prefs": {}}


def get_state():
    """Return the full state dict (read-only recommended)."""
    return _state


def set_user(user):
    """Set current user (dict with id, email, username)."""
    _state["user"] = user


def get_user():
    """Return current user or None."""
    return _state.get("user")


def clear_user():
    """Clear current user (e.g. logout)."""
    _state["user"] = None


def set_pref(key, value):
    """Store a UI preference (e.g. window_geometry)."""
    _state.setdefault("prefs", {})[key] = value


def get_pref(key, default=None):
    """Retrieve a UI preference."""
    return _state.get("prefs", {}).get(key, default)
