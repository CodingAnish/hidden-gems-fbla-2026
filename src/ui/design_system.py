"""
Hidden Gems — Design system (modern startup aesthetic).
Neutral tones, blue primary, rounded components, generous spacing.
FBLA 2026.
"""

# ---- Color palette: modern, neutral, blue accent with depth ----
COLORS = {
    "bg": "#f1f5f9",            # Soft neutral gray
    "bg_elevated": "#ffffff",
    "surface": "#ffffff",
    "surface_hover": "#f8fafc",
    "surface_elevated": "#fefefe",
    "primary": "#2563eb",       # Modern blue
    "primary_hover": "#1d4ed8",
    "primary_pressed": "#1e40af",
    "primary_light": "#dbeafe",
    "primary_gradient_start": "#3b82f6",
    "primary_gradient_end": "#2563eb",
    "secondary": "#64748b",
    "secondary_hover": "#475569",
    "accent": "#06b6d4",        # Teal accent
    "accent_light": "#cffafe",
    "text": "#0f172a",
    "text_secondary": "#64748b",
    "text_muted": "#94a3b8",
    "border": "#e2e8f0",
    "border_focus": "#3b82f6",
    "success": "#10b981",
    "success_light": "#d1fae5",
    "danger": "#ef4444",
    "danger_hover": "#dc2626",
    "danger_light": "#fee2e2",
    "warning": "#f59e0b",
    "info": "#06b6d4",
    "table_header_bg": "#334155",
    "table_header_fg": "#f8fafc",
    "table_row_alt": "#f8fafc",
    "input_bg": "#ffffff",
    "input_border": "#e2e8f0",
    "input_focus_glow": "#bfdbfe",
    "shadow": "rgba(0, 0, 0, 0.1)",
    "shadow_md": "rgba(0, 0, 0, 0.15)",
    "shadow_lg": "rgba(0, 0, 0, 0.2)",
    "nav_bg": "#ffffff",
    "nav_border": "#e2e8f0",
}

# ---- Typography: Inter/Segoe UI with premium hierarchy ----
TYPOGRAPHY = {
    "font_family": "Segoe UI",
    "font_family_fallback": "TkDefaultFont",
    "hero": {"size": 36, "weight": "bold", "line_height": 1.2},
    "title": {"size": 32, "weight": "bold", "line_height": 1.2},
    "heading": {"size": 20, "weight": "bold", "line_height": 1.3},
    "subheading": {"size": 16, "weight": "semibold", "line_height": 1.4},
    "body": {"size": 13, "weight": "normal", "line_height": 1.5},
    "body_large": {"size": 14, "weight": "normal", "line_height": 1.5},
    "caption": {"size": 11, "weight": "normal", "line_height": 1.4},
    "overline": {"size": 10, "weight": "bold", "line_height": 1.3},
}

FONTS = {
    "hero": ("Segoe UI", 36, "bold"),
    "title": ("Segoe UI", 32, "bold"),
    "heading": ("Segoe UI", 20, "bold"),
    "subheading": ("Segoe UI", 16, "bold"),
    "body": ("Segoe UI", 13, "normal"),
    "body_large": ("Segoe UI", 14, "normal"),
    "caption": ("Segoe UI", 11, "normal"),
    "overline": ("Segoe UI", 10, "bold"),
    "nav": ("Segoe UI", 10, "normal"),
}

# ---- Spacing scale: 4, 8, 16, 24, 32, 48 ----
SPACING = {
    "xs": 4,
    "sm": 8,
    "md": 16,
    "lg": 24,
    "xl": 32,
    "xxl": 48,
}

# ---- Border radius: rounded components ----
RADII = {
    "sm": 6,
    "md": 10,
    "lg": 16,
    "xl": 20,
    "full": 9999,
}

# ---- Layout ----
LAYOUT = {
    "content_max_width": 520,
    "content_max_width_wide": 800,
    "min_window_width": 440,
    "min_window_height": 520,
    "table_row_height": 32,
    "input_padding_x": 16,
    "input_padding_y": 12,
    "button_padding_x": 28,
    "button_padding_y": 14,
    "nav_height": 64,
    "bottom_nav_height": 72,
    "hero_height": 200,
}

# ---- Component variants ----
COMPONENT_VARIANTS = {
    "button_primary": {"bg": "primary", "fg": "white", "hover": "primary_hover", "pressed": "primary_pressed"},
    "button_secondary": {"bg": "border", "fg": "text", "hover": "secondary"},
    "button_danger": {"bg": "danger", "fg": "white", "hover": "danger_hover"},
    "card": {"bg": "surface", "border": "border", "shadow": "shadow"},
}

def to_css_vars():
    """Export for web."""
    return {
        "--color-bg": COLORS["bg"],
        "--color-surface": COLORS["surface"],
        "--color-primary": COLORS["primary"],
        "--color-primary-hover": COLORS["primary_hover"],
        "--color-text": COLORS["text"],
        "--color-text-secondary": COLORS["text_secondary"],
        "--color-border": COLORS["border"],
        "--font-family": TYPOGRAPHY["font_family"],
        "--spacing-sm": f"{SPACING['sm']}px",
        "--spacing-md": f"{SPACING['md']}px",
        "--spacing-lg": f"{SPACING['lg']}px",
        "--radius-md": f"{RADII['md']}px",
        "--content-max-width": f"{LAYOUT['content_max_width']}px",
    }
