"""
Modern action card components — mobile-app-inspired UI elements.
Icons, shadows, hover animations, rounded corners. FBLA 2026.
"""
import tkinter as tk
from ..design_system import COLORS, FONTS, SPACING, RADII

HOVER_SCALE_DURATION = 100


def ActionCard(parent, icon, title, subtitle=None, command=None, color_accent=None):
    """
    Mobile-app-style action card: icon + text + hover animation.
    Returns a frame that acts as a clickable card.
    """
    accent = color_accent or COLORS["primary"]
    bg_default = COLORS["surface"]
    bg_hover = COLORS["surface_hover"]
    
    # Outer wrapper for shadow
    wrapper = tk.Frame(parent, bg=parent["bg"], highlightthickness=0)
    
    # Shadow layers (soft depth)
    shadow1 = tk.Frame(wrapper, bg="#e5e7eb", highlightthickness=0)
    shadow1.place(x=0, y=4, relwidth=1, relheight=1)
    shadow2 = tk.Frame(wrapper, bg="#d1d5db", highlightthickness=0)
    shadow2.place(x=0, y=2, relwidth=1, relheight=1)
    
    # Main card
    card = tk.Frame(
        wrapper,
        bg=bg_default,
        highlightthickness=1,
        highlightbackground=COLORS["border"],
        cursor="hand2",
    )
    card.place(x=0, y=0, relwidth=1, relheight=1)
    
    # Content
    content = tk.Frame(card, bg=bg_default)
    content.pack(fill=tk.BOTH, expand=True, padx=SPACING["lg"], pady=SPACING["lg"])
    
    # Icon (emoji or Unicode symbol)
    icon_label = tk.Label(
        content,
        text=icon,
        font=("Segoe UI Emoji", 32, "normal"),
        fg=accent,
        bg=bg_default,
    )
    icon_label.pack(pady=(SPACING["sm"], SPACING["md"]))
    
    # Title
    title_label = tk.Label(
        content,
        text=title,
        font=FONTS["body_large"],
        fg=COLORS["text"],
        bg=bg_default,
    )
    title_label.pack()
    
    # Optional subtitle
    if subtitle:
        subtitle_label = tk.Label(
            content,
            text=subtitle,
            font=FONTS["caption"],
            fg=COLORS["text_secondary"],
            bg=bg_default,
        )
        subtitle_label.pack(pady=(SPACING["xs"], 0))
    
    # Hover animation
    def on_enter(e):
        card["bg"] = bg_hover
        content["bg"] = bg_hover
        icon_label["bg"] = bg_hover
        title_label["bg"] = bg_hover
        if subtitle:
            subtitle_label["bg"] = bg_hover
        shadow1.place(x=0, y=6, relwidth=1, relheight=1)
    
    def on_leave(e):
        card["bg"] = bg_default
        content["bg"] = bg_default
        icon_label["bg"] = bg_default
        title_label["bg"] = bg_default
        if subtitle:
            subtitle_label["bg"] = bg_default
        shadow1.place(x=0, y=4, relwidth=1, relheight=1)
    
    def on_click(e):
        if command:
            wrapper.after(50, command)
    
    for widget in [card, content, icon_label, title_label] + ([subtitle_label] if subtitle else []):
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
        widget.bind("<Button-1>", on_click)
    
    return wrapper


def HeaderCard(parent, title, subtitle, user_info=None):
    """
    App header card — prominent title, subtitle, optional user info.
    Returns the card frame.
    """
    card = tk.Frame(
        parent,
        bg=COLORS["surface"],
        highlightthickness=1,
        highlightbackground=COLORS["border"],
    )
    card.pack(fill=tk.X, pady=(0, SPACING["xl"]))
    
    # Shadow
    shadow = tk.Frame(parent, bg="#d1d5db", highlightthickness=0)
    shadow.place(in_=card, x=0, y=3, relwidth=1, relheight=1)
    card.lift()
    
    content = tk.Frame(card, bg=COLORS["surface"])
    content.pack(fill=tk.X, padx=SPACING["xl"], pady=SPACING["lg"])
    
    tk.Label(
        content,
        text=title,
        font=FONTS["title"],
        fg=COLORS["text"],
        bg=COLORS["surface"],
    ).pack(anchor=tk.W, pady=(0, SPACING["xs"]))
    
    tk.Label(
        content,
        text=subtitle,
        font=FONTS["caption"],
        fg=COLORS["text_secondary"],
        bg=COLORS["surface"],
    ).pack(anchor=tk.W, pady=(0, SPACING["sm"] if user_info else 0))
    
    if user_info:
        tk.Label(
            content,
            text=user_info,
            font=FONTS["caption"],
            fg=COLORS["text_muted"],
            bg=COLORS["surface"],
        ).pack(anchor=tk.W)
    
    return card
