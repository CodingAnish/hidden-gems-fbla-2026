"""
Theme application — applies design system to Tkinter/ttk.
Call setup_theme() once at startup. FBLA 2026.
"""
import tkinter as tk
from tkinter import ttk

from .design_system import COLORS, FONTS, SPACING, LAYOUT

# Backward compatibility
CONTENT_MAX_WIDTH = LAYOUT["content_max_width"]
PAD = {"pady": SPACING["md"], "padx": SPACING["sm"]}
PAD_SM = {"pady": SPACING["xs"], "padx": SPACING["xs"]}
PAD_LG = {"pady": SPACING["lg"], "padx": SPACING["lg"]}


def setup_theme(root=None):
    """Apply modern ttk styles. Call once at app startup (before creating windows)."""
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    # ---- Frame ----
    style.configure("TFrame", background=COLORS["bg"])
    style.configure(
        "Card.TFrame",
        background=COLORS["surface"],
        relief="flat",
    )

    # ---- Labels ----
    style.configure(
        "TLabel",
        background=COLORS["bg"],
        foreground=COLORS["text"],
        font=FONTS["body"],
        padding=(0, 4),
    )
    style.configure(
        "Title.TLabel",
        background=COLORS["bg"],
        foreground=COLORS["text"],
        font=FONTS["title"],
        padding=(0, 8),
    )
    style.configure(
        "Heading.TLabel",
        background=COLORS["bg"],
        foreground=COLORS["text"],
        font=FONTS["heading"],
        padding=(0, 6),
    )
    style.configure(
        "Subheading.TLabel",
        background=COLORS["bg"],
        foreground=COLORS["text"],
        font=FONTS["subheading"],
        padding=(0, 4),
    )
    style.configure(
        "Caption.TLabel",
        background=COLORS["bg"],
        foreground=COLORS["text_secondary"],
        font=FONTS["caption"],
        padding=(0, 2),
    )
    for name, font_key in [
        ("Card.Title.TLabel", "title"),
        ("Card.Heading.TLabel", "heading"),
        ("Card.Subheading.TLabel", "subheading"),
        ("Card.Caption.TLabel", "caption"),
    ]:
        style.configure(
            name,
            background=COLORS["surface"],
            foreground=COLORS["text"] if "Caption" not in name else COLORS["text_secondary"],
            font=FONTS[font_key],
            padding=(0, 8) if "Title" in name else (0, 4),
        )

    # ---- Buttons (ttk fallback for widgets that need ttk) ----
    style.configure(
        "TButton",
        font=FONTS["body"],
        padding=(LAYOUT["button_padding_x"], LAYOUT["button_padding_y"]),
        background=COLORS["primary"],
        foreground="white",
    )
    style.map(
        "TButton",
        background=[("active", COLORS["primary_hover"]), ("pressed", COLORS["primary_hover"])],
        foreground=[("active", "white"), ("pressed", "white")],
    )
    style.configure(
        "Primary.TButton",
        font=FONTS["body"],
        padding=(LAYOUT["button_padding_x"], LAYOUT["button_padding_y"]),
        background=COLORS["primary"],
        foreground="white",
    )
    style.map(
        "Primary.TButton",
        background=[("active", COLORS["primary_hover"]), ("pressed", COLORS["primary_hover"])],
        foreground=[("active", "white"), ("pressed", "white")],
    )
    style.configure(
        "Secondary.TButton",
        font=FONTS["body"],
        padding=(LAYOUT["button_padding_x"], LAYOUT["button_padding_y"]),
        background=COLORS["border"],
        foreground=COLORS["text"],
    )
    style.map(
        "Secondary.TButton",
        background=[("active", COLORS["secondary"]), ("pressed", COLORS["secondary"])],
        foreground=[("active", "white"), ("pressed", "white")],
    )
    style.configure(
        "Danger.TButton",
        font=FONTS["body"],
        padding=(LAYOUT["button_padding_x"], LAYOUT["button_padding_y"]),
        background=COLORS["danger"],
        foreground="white",
    )
    style.map(
        "Danger.TButton",
        background=[("active", COLORS["danger_hover"]), ("pressed", COLORS["danger_hover"])],
        foreground=[("active", "white"), ("pressed", "white")],
    )

    # ---- Entry ----
    style.configure(
        "TEntry",
        font=FONTS["body"],
        fieldbackground=COLORS["input_bg"],
        foreground=COLORS["text"],
        padding=LAYOUT["input_padding_y"],
        insertcolor=COLORS["text"],
        borderwidth=1,
    )

    # ---- Combobox ----
    style.configure(
        "TCombobox",
        font=FONTS["body"],
        fieldbackground=COLORS["input_bg"],
        foreground=COLORS["text"],
        padding=8,
        arrowcolor=COLORS["text"],
    )
    style.map("TCombobox", fieldbackground=[("readonly", COLORS["input_bg"])])

    # ---- Treeview ----
    style.configure(
        "Treeview",
        font=FONTS["body"],
        background=COLORS["surface"],
        foreground=COLORS["text"],
        fieldbackground=COLORS["surface"],
        rowheight=LAYOUT["table_row_height"],
        borderwidth=0,
    )
    style.configure(
        "Treeview.Heading",
        font=(FONTS["body"][0], 11, "bold"),
        background=COLORS["table_header_bg"],
        foreground=COLORS["table_header_fg"],
        padding=(LAYOUT["input_padding_x"], LAYOUT["input_padding_y"]),
        borderwidth=0,
    )
    style.map(
        "Treeview",
        background=[("selected", COLORS["primary"])],
        foreground=[("selected", "white")],
    )
    style.map("Treeview.Heading", background=[("active", COLORS["border"])])

    # ---- Separator ----
    style.configure("TSeparator", background=COLORS["border"])

    # ---- Scrollbar ----
    style.configure(
        "Vertical.TScrollbar",
        background=COLORS["border"],
        troughcolor=COLORS["bg"],
        borderwidth=0,
        arrowsize=0,
    )


def apply_window_bg(win, bg=None):
    """Set root/toplevel window background (ttk doesn't set this)."""
    win.configure(bg=bg or COLORS["bg"])


def make_section_label(parent, text, style_class="Subheading.TLabel"):
    """Create a section heading label."""
    return ttk.Label(parent, text=text, style=style_class)
