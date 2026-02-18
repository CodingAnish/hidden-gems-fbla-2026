"""
Themed button components — rounded, modern, smooth transitions.
Startup dashboard aesthetic. FBLA 2026.
"""
import tkinter as tk
from ..design_system import COLORS, FONTS, LAYOUT, RADII

FEEDBACK_DELAY_MS = 50


def _with_feedback(command):
    """Run command after brief delay for visual feedback."""
    if not command:
        return None
    def run(widget):
        top = widget.winfo_toplevel()
        top.after(FEEDBACK_DELAY_MS, command)
    return run


def _make_rounded_button(parent, text, bg, fg, hover_bg, pressed_bg, command=None, **kwargs):
    """Internal: create rounded button with hover and press states."""
    cmd = _with_feedback(command)
    
    # Create a Frame wrapper for rounded appearance via a Canvas
    wrapper = tk.Frame(parent, bg=bg, highlightthickness=0)
    
    btn = tk.Button(
        wrapper,
        text=text,
        command=lambda: cmd(btn) if cmd else None,
        bg=bg,
        fg=fg,
        activebackground=pressed_bg,
        activeforeground=fg,
        font=FONTS["body"],
        relief=tk.FLAT,
        borderwidth=0,
        highlightthickness=0,
        padx=LAYOUT["button_padding_x"],
        pady=LAYOUT["button_padding_y"],
        cursor="hand2",
        **kwargs,
    )
    btn.pack(fill=tk.BOTH, expand=True)
    
    # State tracking
    btn._normal_bg = bg
    btn._hover_bg = hover_bg
    btn._pressed_bg = pressed_bg
    btn._fg = fg
    
    def on_enter(e):
        btn["bg"] = hover_bg
        wrapper["bg"] = hover_bg
    
    def on_leave(e):
        btn["bg"] = bg
        wrapper["bg"] = bg
    
    def on_press(e):
        btn["bg"] = pressed_bg
        wrapper["bg"] = pressed_bg
    
    def on_release(e):
        if btn.winfo_containing(e.x_root, e.y_root) == btn:
            btn["bg"] = hover_bg
            wrapper["bg"] = hover_bg
        else:
            btn["bg"] = bg
            wrapper["bg"] = bg
    
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    btn.bind("<ButtonPress-1>", on_press)
    btn.bind("<ButtonRelease-1>", on_release)
    
    return wrapper


def PrimaryButton(parent, text, command=None, **kwargs):
    """Primary action button — modern blue, rounded."""
    return _make_rounded_button(
        parent, text,
        bg=COLORS["primary"],
        fg="white",
        hover_bg=COLORS["primary_hover"],
        pressed_bg=COLORS["primary_pressed"],
        command=command,
        **kwargs
    )


def SecondaryButton(parent, text, command=None, **kwargs):
    """Secondary action — gray outline style."""
    return _make_rounded_button(
        parent, text,
        bg=COLORS["surface"],
        fg=COLORS["text"],
        hover_bg=COLORS["surface_hover"],
        pressed_bg=COLORS["border"],
        command=command,
        **kwargs
    )


def DangerButton(parent, text, command=None, **kwargs):
    """Destructive action — red."""
    return _make_rounded_button(
        parent, text,
        bg=COLORS["danger"],
        fg="white",
        hover_bg=COLORS["danger_hover"],
        pressed_bg=COLORS["danger_hover"],
        command=command,
        **kwargs
    )
