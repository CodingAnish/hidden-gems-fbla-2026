"""
Hero section and enhanced card components for premium UI.
FBLA 2026 Hidden Gems.
"""
import tkinter as tk
from ..design_system import COLORS, FONTS, SPACING, LAYOUT


def HeroSection(parent, title, subtitle, on_search=None, placeholder="Search businesses..."):
    """
    Hero section with gradient background, large title, search bar.
    Creates emotional impact and immediate functionality.
    """
    # Container with gradient simulation (layered frames)
    hero = tk.Frame(parent, bg=COLORS["primary"], height=LAYOUT["hero_height"])
    hero.pack(fill=tk.X, pady=(0, SPACING["xl"]))
    hero.pack_propagate(False)
    
    # Content
    content = tk.Frame(hero, bg=COLORS["primary"])
    content.pack(fill=tk.BOTH, expand=True, padx=SPACING["xl"], pady=SPACING["xl"])
    
    # Title
    tk.Label(
        content,
        text=title,
        font=FONTS["hero"],
        fg=COLORS["surface"],
        bg=COLORS["primary"],
    ).pack(pady=(SPACING["md"], SPACING["xs"]))
    
    # Subtitle
    tk.Label(
        content,
        text=subtitle,
        font=FONTS["body_large"],
        fg=COLORS["primary_light"],
        bg=COLORS["primary"],
    ).pack(pady=(0, SPACING["lg"]))
    
    # Search bar (if enabled)
    if on_search:
        search_frame = tk.Frame(
            content,
            bg=COLORS["surface"],
            highlightthickness=0,
        )
        search_frame.pack(fill=tk.X, padx=SPACING["xl"])
        
        search_entry = tk.Entry(
            search_frame,
            bg=COLORS["surface"],
            fg=COLORS["text"],
            font=FONTS["body"],
            relief=tk.FLAT,
            borderwidth=0,
            insertbackground=COLORS["text"],
        )
        search_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=SPACING["md"], pady=SPACING["md"])
        search_entry.insert(0, placeholder)
        search_entry.config(fg=COLORS["text_muted"])
        
        # Placeholder behavior
        def on_focus_in(e):
            if search_entry.get() == placeholder:
                search_entry.delete(0, tk.END)
                search_entry.config(fg=COLORS["text"])
        
        def on_focus_out(e):
            if not search_entry.get():
                search_entry.insert(0, placeholder)
                search_entry.config(fg=COLORS["text_muted"])
        
        search_entry.bind("<FocusIn>", on_focus_in)
        search_entry.bind("<FocusOut>", on_focus_out)
        search_entry.bind("<Return>", lambda e: on_search(search_entry.get()) if search_entry.get() != placeholder else None)
        
        # Search icon
        search_icon = tk.Label(
            search_frame,
            text="🔍",
            font=("Segoe UI Emoji", 16, "normal"),
            bg=COLORS["surface"],
            cursor="hand2",
        )
        search_icon.pack(side=tk.RIGHT, padx=SPACING["md"])
        search_icon.bind("<Button-1>", lambda e: on_search(search_entry.get()) if search_entry.get() != placeholder else None)
    
    return hero


def PremiumCard(parent, icon, title, description, command=None, color_accent=None, show_arrow=True):
    """
    Enhanced card with icon, title, description, arrow, and lift animation.
    Feels clickable like a card, not like a button.
    """
    accent = color_accent or COLORS["primary"]
    bg_default = COLORS["surface"]
    bg_hover = COLORS["surface_hover"]
    
    # Wrapper for shadow
    wrapper = tk.Frame(parent, bg=parent["bg"], highlightthickness=0)
    
    # Multi-layer shadow
    shadow3 = tk.Frame(wrapper, bg="#e5e7eb", highlightthickness=0)
    shadow3.place(x=0, y=6, relwidth=1, relheight=1)
    shadow2 = tk.Frame(wrapper, bg="#d1d5db", highlightthickness=0)
    shadow2.place(x=0, y=3, relwidth=1, relheight=1)
    
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
    
    # Top row: Icon + Title + Arrow
    top_row = tk.Frame(content, bg=bg_default)
    top_row.pack(fill=tk.X, pady=(0, SPACING["sm"]))
    
    # Icon
    icon_label = tk.Label(
        top_row,
        text=icon,
        font=("Segoe UI Emoji", 28, "normal"),
        fg=accent,
        bg=bg_default,
    )
    icon_label.pack(side=tk.LEFT, padx=(0, SPACING["md"]))
    
    # Title
    title_label = tk.Label(
        top_row,
        text=title,
        font=FONTS["subheading"],
        fg=COLORS["text"],
        bg=bg_default,
    )
    title_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    # Arrow
    if show_arrow:
        arrow_label = tk.Label(
            top_row,
            text="→",
            font=FONTS["heading"],
            fg=COLORS["text_muted"],
            bg=bg_default,
        )
        arrow_label.pack(side=tk.RIGHT)
    
    # Description
    desc_label = tk.Label(
        content,
        text=description,
        font=FONTS["caption"],
        fg=COLORS["text_secondary"],
        bg=bg_default,
        wraplength=400,
        justify=tk.LEFT,
    )
    desc_label.pack(fill=tk.X, anchor=tk.W)
    
    # Hover lift animation
    def on_enter(e):
        card["bg"] = bg_hover
        content["bg"] = bg_hover
        top_row["bg"] = bg_hover
        icon_label["bg"] = bg_hover
        title_label["bg"] = bg_hover
        desc_label["bg"] = bg_hover
        if show_arrow:
            arrow_label["bg"] = bg_hover
            arrow_label["fg"] = accent
        # Lift shadow
        shadow3.place(x=0, y=10, relwidth=1, relheight=1)
        shadow2.place(x=0, y=5, relwidth=1, relheight=1)
    
    def on_leave(e):
        card["bg"] = bg_default
        content["bg"] = bg_default
        top_row["bg"] = bg_default
        icon_label["bg"] = bg_default
        title_label["bg"] = bg_default
        desc_label["bg"] = bg_default
        if show_arrow:
            arrow_label["bg"] = bg_default
            arrow_label["fg"] = COLORS["text_muted"]
        # Reset shadow
        shadow3.place(x=0, y=6, relwidth=1, relheight=1)
        shadow2.place(x=0, y=3, relwidth=1, relheight=1)
    
    def on_press(e):
        # Press feedback: scale down slightly (simulated by adjusting shadow)
        shadow3.place(x=0, y=2, relwidth=1, relheight=1)
        shadow2.place(x=0, y=1, relwidth=1, relheight=1)
    
    def on_release(e):
        on_enter(e)  # Return to hover state
        if command:
            wrapper.after(50, command)
    
    widgets = [card, content, top_row, icon_label, title_label, desc_label]
    if show_arrow:
        widgets.append(arrow_label)
    
    for widget in widgets:
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
        widget.bind("<ButtonPress-1>", on_press)
        widget.bind("<ButtonRelease-1>", on_release)
    
    return wrapper


def FeaturedCard(parent, business_name, category, rating, on_click=None):
    """
    Compact featured business card for content previews.
    """
    card = tk.Frame(
        parent,
        bg=COLORS["surface"],
        highlightthickness=1,
        highlightbackground=COLORS["border"],
        cursor="hand2",
    )
    
    content = tk.Frame(card, bg=COLORS["surface"])
    content.pack(fill=tk.BOTH, expand=True, padx=SPACING["md"], pady=SPACING["md"])
    
    # Name
    tk.Label(
        content,
        text=business_name,
        font=FONTS["body_large"],
        fg=COLORS["text"],
        bg=COLORS["surface"],
    ).pack(anchor=tk.W, pady=(0, SPACING["xs"]))
    
    # Category + Rating
    info = tk.Frame(content, bg=COLORS["surface"])
    info.pack(fill=tk.X)
    
    tk.Label(
        info,
        text=category,
        font=FONTS["caption"],
        fg=COLORS["text_secondary"],
        bg=COLORS["surface"],
    ).pack(side=tk.LEFT)
    
    tk.Label(
        info,
        text=f"⭐ {rating}",
        font=FONTS["caption"],
        fg=COLORS["warning"],
        bg=COLORS["surface"],
    ).pack(side=tk.RIGHT)
    
    if on_click:
        card.bind("<Button-1>", lambda e: on_click())
    
    return card
