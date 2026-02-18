"""
Layout components — rounded cards with soft shadows, modern spacing.
FBLA 2026.
"""
import tkinter as tk
from ..design_system import COLORS, LAYOUT, SPACING, RADII


def make_centered_content(parent, max_width=None, pad=24, min_height=None):
    """
    Outer container and centered content area.
    Returns (outer_frame, content_frame).
    """
    max_width = max_width or LAYOUT["content_max_width"]
    min_height = min_height or LAYOUT["min_window_height"]
    outer = tk.Frame(parent, bg=COLORS["bg"], padx=pad, pady=pad)
    outer.pack(fill=tk.BOTH, expand=True)
    content = tk.Frame(outer, bg=COLORS["bg"], width=max_width, height=min_height)
    content.pack(expand=True)
    content.pack_propagate(False)
    return outer, content


def make_card_container(parent, bg=None, padx=24, pady=24):
    """
    Card-style container (elevated surface) with rounded corners.
    Returns a tk.Frame.
    """
    bg = bg or COLORS["surface"]
    card = tk.Frame(parent, bg=bg, padx=padx, pady=pady, highlightthickness=0)
    return card


def make_centered_card(parent, max_width=None, outer_pad=32, min_height=None):
    """
    Centered card with soft shadow — modern dashboard aesthetic.
    Returns (outer_frame, card_frame). Pack content into card_frame.
    """
    max_width = max_width or LAYOUT["content_max_width"]
    min_height = min_height or LAYOUT["min_window_height"]
    
    outer = tk.Frame(parent, bg=COLORS["bg"], padx=outer_pad, pady=outer_pad)
    outer.pack(fill=tk.BOTH, expand=True)
    
    center = tk.Frame(outer, bg=COLORS["bg"], width=max_width, height=min_height)
    center.pack(expand=True)
    center.pack_propagate(False)
    
    # Subtle shadow: multiple offset layers for soft depth
    for offset, color in [(6, "#ddd"), (4, "#e5e5e5"), (2, "#efefef")]:
        shadow = tk.Frame(center, bg=color, highlightthickness=0)
        shadow.place(x=offset, y=offset, width=max_width - offset, height=min_height - offset)
    
    # Card: white surface, minimal border, rounded via config (Tkinter doesn't support CSS border-radius,
    # so we simulate with a very light border and clean background)
    card = tk.Frame(
        center,
        bg=COLORS["surface"],
        padx=SPACING["xl"],
        pady=SPACING["xl"],
        highlightthickness=1,
        highlightbackground=COLORS["border"],
        highlightcolor=COLORS["border"],
    )
    card.pack(fill=tk.BOTH, expand=True)
    card.lift()
    
    return outer, card
