"""
Micro-interactions: toasts, loading states, focus glows, animations.
FBLA 2026 Hidden Gems.
"""
import tkinter as tk
from ..design_system import COLORS, FONTS, SPACING


class ToastNotification:
    """
    Toast notification system for feedback messages.
    """
    _active_toasts = []
    
    @classmethod
    def show(cls, parent, message, toast_type="info", duration=3000):
        """
        Show a toast notification.
        Types: info, success, warning, error
        """
        # Position from top
        y_offset = 80 + (len(cls._active_toasts) * 70)
        
        # Colors by type
        colors = {
            "info": (COLORS["info"], COLORS["surface"]),
            "success": (COLORS["success"], COLORS["surface"]),
            "warning": (COLORS["warning"], COLORS["surface"]),
            "error": (COLORS["danger"], COLORS["surface"]),
        }
        bg_color, fg_color = colors.get(toast_type, colors["info"])
        
        # Toast frame
        toast = tk.Frame(
            parent,
            bg=bg_color,
            highlightthickness=0,
        )
        toast.place(x=20, y=y_offset, width=320, height=56)
        
        # Shadow
        shadow = tk.Frame(parent, bg="#94a3b8", highlightthickness=0)
        shadow.place(x=20, y=y_offset + 2, width=320, height=56)
        toast.lift()
        
        # Content
        content = tk.Frame(toast, bg=bg_color)
        content.pack(fill=tk.BOTH, expand=True, padx=SPACING["md"], pady=SPACING["md"])
        
        # Icon
        icons = {
            "info": "ℹ️",
            "success": "✅",
            "warning": "⚠️",
            "error": "❌",
        }
        icon = tk.Label(
            content,
            text=icons.get(toast_type, "ℹ️"),
            font=("Segoe UI Emoji", 18, "normal"),
            bg=bg_color,
        )
        icon.pack(side=tk.LEFT, padx=(0, SPACING["sm"]))
        
        # Message
        tk.Label(
            content,
            text=message,
            font=FONTS["body"],
            fg=fg_color,
            bg=bg_color,
            wraplength=240,
        ).pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        cls._active_toasts.append(toast)
        
        # Auto-dismiss
        def dismiss():
            try:
                toast.destroy()
                shadow.destroy()
                if toast in cls._active_toasts:
                    cls._active_toasts.remove(toast)
            except:
                pass
        
        parent.after(duration, dismiss)
        
        return toast


def EnhancedEntry(parent, width=None, show=None, placeholder="", **kwargs):
    """
    Entry with focus glow and enhanced interactions.
    """
    wrapper = tk.Frame(parent, bg=COLORS["surface"], highlightthickness=0)
    
    # Outer glow frame (hidden by default)
    glow_frame = tk.Frame(
        wrapper,
        bg=COLORS["input_focus_glow"],
        highlightthickness=0,
    )
    
    # Entry frame
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
    
    # Placeholder
    if placeholder:
        entry.insert(0, placeholder)
        entry.config(fg=COLORS["text_muted"])
        
        def on_focus_in_placeholder(e):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(fg=COLORS["text"])
            # Show glow
            glow_frame.place(x=-3, y=-3, relwidth=1, relheight=1, width=6, height=6)
            entry_frame.lift()
        
        def on_focus_out_placeholder(e):
            if not entry.get():
                entry.insert(0, placeholder)
                entry.config(fg=COLORS["text_muted"])
            # Hide glow
            glow_frame.place_forget()
        
        entry.bind("<FocusIn>", on_focus_in_placeholder)
        entry.bind("<FocusOut>", on_focus_out_placeholder)
    else:
        def on_focus_in(e):
            glow_frame.place(x=-3, y=-3, relwidth=1, relheight=1, width=6, height=6)
            entry_frame.lift()
            entry_frame["highlightbackground"] = COLORS["border_focus"]
        
        def on_focus_out(e):
            glow_frame.place_forget()
            entry_frame["highlightbackground"] = COLORS["input_border"]
        
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
    
    wrapper.entry = entry
    return wrapper


def LoadingSpinner(parent, size=32):
    """
    Simple loading indicator.
    """
    spinner = tk.Label(
        parent,
        text="⏳",
        font=("Segoe UI Emoji", size, "normal"),
        fg=COLORS["primary"],
        bg=parent["bg"],
    )
    return spinner


def EmptyState(parent, icon, title, subtitle):
    """
    Empty state component for when no content exists.
    """
    container = tk.Frame(parent, bg=COLORS["surface"])
    container.pack(fill=tk.BOTH, expand=True, pady=SPACING["xxl"])
    
    # Icon
    tk.Label(
        container,
        text=icon,
        font=("Segoe UI Emoji", 48, "normal"),
        fg=COLORS["text_muted"],
        bg=COLORS["surface"],
    ).pack(pady=(SPACING["xxl"], SPACING["lg"]))
    
    # Title
    tk.Label(
        container,
        text=title,
        font=FONTS["heading"],
        fg=COLORS["text_secondary"],
        bg=COLORS["surface"],
    ).pack(pady=(0, SPACING["sm"]))
    
    # Subtitle
    tk.Label(
        container,
        text=subtitle,
        font=FONTS["caption"],
        fg=COLORS["text_muted"],
        bg=COLORS["surface"],
    ).pack()
    
    return container
