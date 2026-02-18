"""
Navigation components — top bar, bottom bar, modern mobile-style navigation.
FBLA 2026 Hidden Gems.
"""
import tkinter as tk
from ..design_system import COLORS, FONTS, SPACING, LAYOUT

def TopNavBar(parent, title="Hidden Gems", user=None, on_profile_click=None):
    """
    Top navigation bar with app branding, user avatar, subtle shadow.
    """
    nav = tk.Frame(parent, bg=COLORS["nav_bg"], height=LAYOUT["nav_height"])
    nav.pack(side=tk.TOP, fill=tk.X)
    nav.pack_propagate(False)
    
    # Shadow layer
    shadow = tk.Frame(parent, bg=COLORS["border"], height=1)
    shadow.pack(side=tk.TOP, fill=tk.X)
    
    # Content container
    content = tk.Frame(nav, bg=COLORS["nav_bg"])
    content.pack(fill=tk.BOTH, expand=True, padx=SPACING["xl"], pady=SPACING["md"])
    
    # Left: App branding
    left = tk.Frame(content, bg=COLORS["nav_bg"])
    left.pack(side=tk.LEFT, fill=tk.Y)
    
    # Icon
    icon = tk.Label(
        left,
        text="💎",
        font=("Segoe UI Emoji", 24, "normal"),
        bg=COLORS["nav_bg"],
    )
    icon.pack(side=tk.LEFT, padx=(0, SPACING["sm"]))
    
    # Title
    tk.Label(
        left,
        text=title,
        font=FONTS["heading"],
        fg=COLORS["text"],
        bg=COLORS["nav_bg"],
    ).pack(side=tk.LEFT)
    
    # Right: User avatar
    if user:
        right = tk.Frame(content, bg=COLORS["nav_bg"])
        right.pack(side=tk.RIGHT, fill=tk.Y)
        
        username = user.get("username", user.get("email", "User"))
        initials = username[0].upper() if username else "U"
        
        # Avatar circle
        avatar_frame = tk.Frame(right, bg=COLORS["nav_bg"])
        avatar_frame.pack(side=tk.RIGHT)
        
        avatar = tk.Label(
            avatar_frame,
            text=initials,
            font=FONTS["subheading"],
            fg=COLORS["surface"],
            bg=COLORS["primary"],
            width=3,
            height=1,
            cursor="hand2",
        )
        avatar.pack(padx=SPACING["xs"], pady=SPACING["xs"])
        
        if on_profile_click:
            avatar.bind("<Button-1>", lambda e: on_profile_click())
        
        # Username
        tk.Label(
            right,
            text=username[:12],
            font=FONTS["caption"],
            fg=COLORS["text_secondary"],
            bg=COLORS["nav_bg"],
        ).pack(side=tk.RIGHT, padx=(0, SPACING["sm"]))
    
    return nav


def BottomNavBar(parent, active="home", on_nav_click=None):
    """
    Bottom navigation bar with icon tabs — mobile-style navigation.
    """
    nav = tk.Frame(parent, bg=COLORS["nav_bg"], height=LAYOUT["bottom_nav_height"])
    nav.pack(side=tk.BOTTOM, fill=tk.X)
    nav.pack_propagate(False)
    
    # Top border shadow
    shadow = tk.Frame(parent, bg=COLORS["border"], height=1)
    shadow.pack(side=tk.BOTTOM, fill=tk.X)
    
    # Content
    content = tk.Frame(nav, bg=COLORS["nav_bg"])
    content.pack(fill=tk.BOTH, expand=True, pady=SPACING["sm"])
    
    tabs = [
        {"id": "home", "icon": "🏠", "label": "Home"},
        {"id": "browse", "icon": "🔍", "label": "Browse"},
        {"id": "favorites", "icon": "❤️", "label": "Favorites"},
        {"id": "profile", "icon": "👤", "label": "Profile"},
    ]
    
    for tab in tabs:
        is_active = (tab["id"] == active)
        tab_frame = tk.Frame(content, bg=COLORS["nav_bg"])
        tab_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        btn_container = tk.Frame(tab_frame, bg=COLORS["nav_bg"])
        btn_container.pack(expand=True)
        
        # Icon
        icon_label = tk.Label(
            btn_container,
            text=tab["icon"],
            font=("Segoe UI Emoji", 20, "normal"),
            fg=COLORS["primary"] if is_active else COLORS["text_secondary"],
            bg=COLORS["nav_bg"],
            cursor="hand2",
        )
        icon_label.pack()
        
        # Label
        text_label = tk.Label(
            btn_container,
            text=tab["label"],
            font=FONTS["nav"],
            fg=COLORS["primary"] if is_active else COLORS["text_muted"],
            bg=COLORS["nav_bg"],
            cursor="hand2",
        )
        text_label.pack(pady=(SPACING["xs"], 0))
        
        # Hover and click
        def make_handler(tab_id):
            def on_click(e):
                if on_nav_click:
                    on_nav_click(tab_id)
            
            def on_enter(e):
                if tab_id != active:
                    icon_label["fg"] = COLORS["primary_hover"]
                    text_label["fg"] = COLORS["text_secondary"]
            
            def on_leave(e):
                if tab_id != active:
                    icon_label["fg"] = COLORS["text_secondary"]
                    text_label["fg"] = COLORS["text_muted"]
            
            return on_click, on_enter, on_leave
        
        click_handler, enter_handler, leave_handler = make_handler(tab["id"])
        
        for widget in [icon_label, text_label]:
            widget.bind("<Button-1>", click_handler)
            if not is_active:
                widget.bind("<Enter>", enter_handler)
                widget.bind("<Leave>", leave_handler)
    
    return nav
