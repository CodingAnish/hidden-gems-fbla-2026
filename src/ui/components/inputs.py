"""
Modern input components — focus borders, rounded, clean.
FBLA 2026.
"""
import tkinter as tk
from tkinter import ttk
from ..design_system import COLORS, FONTS, LAYOUT, SPACING


def ModernEntry(parent, width=None, show=None, **kwargs):
    """
    Styled entry with focus border and modern appearance.
    Returns a Frame containing the entry (use .get() on the returned wrapper's entry child).
    """
    wrapper = tk.Frame(parent, bg=COLORS["surface"], highlightthickness=0)
    
    entry_frame = tk.Frame(
        wrapper,
        bg=COLORS["input_bg"],
        highlightthickness=2,
        highlightbackground=COLORS["input_border"],
        highlightcolor=COLORS["border_focus"],
    )
    entry_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
    
    entry = tk.Entry(
        entry_frame,
        bg=COLORS["input_bg"],
        fg=COLORS["text"],
        font=FONTS["body"],
        relief=tk.FLAT,
        borderwidth=0,
        insertbackground=COLORS["text"],
        show=show,
        **kwargs
    )
    entry.pack(fill=tk.BOTH, expand=True, padx=LAYOUT["input_padding_x"], pady=LAYOUT["input_padding_y"])
    
    def on_focus_in(e):
        entry_frame["highlightbackground"] = COLORS["border_focus"]
        entry_frame["highlightcolor"] = COLORS["border_focus"]
    
    def on_focus_out(e):
        entry_frame["highlightbackground"] = COLORS["input_border"]
        entry_frame["highlightcolor"] = COLORS["input_border"]
    
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)
    
    # Expose entry for external access
    wrapper.entry = entry
    return wrapper


def ModernLabel(parent, text, style="body", **kwargs):
    """
    Styled label with proper typography.
    style: "title", "heading", "subheading", "body", "caption"
    """
    font_map = {
        "title": FONTS["title"],
        "heading": FONTS["heading"],
        "subheading": FONTS["subheading"],
        "body": FONTS["body"],
        "caption": FONTS["caption"],
    }
    fg_map = {
        "title": COLORS["text"],
        "heading": COLORS["text"],
        "subheading": COLORS["text"],
        "body": COLORS["text"],
        "caption": COLORS["text_secondary"],
    }
    return tk.Label(
        parent,
        text=text,
        font=font_map.get(style, FONTS["body"]),
        fg=fg_map.get(style, COLORS["text"]),
        bg=COLORS["surface"],
        **kwargs
    )
