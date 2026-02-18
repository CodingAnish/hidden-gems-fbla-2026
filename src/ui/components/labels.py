"""
Themed label components — typography hierarchy.
FBLA 2026.
"""
from tkinter import ttk


def TitleLabel(parent, text, **kwargs):
    """Page/screen title."""
    return ttk.Label(parent, text=text, style="Title.TLabel", **kwargs)


def HeadingLabel(parent, text, **kwargs):
    """Section heading."""
    return ttk.Label(parent, text=text, style="Heading.TLabel", **kwargs)


def SubheadingLabel(parent, text, **kwargs):
    """Subsection or card title."""
    return ttk.Label(parent, text=text, style="Subheading.TLabel", **kwargs)


def CaptionLabel(parent, text, **kwargs):
    """Secondary/muted text."""
    return ttk.Label(parent, text=text, style="Caption.TLabel", **kwargs)


# Card context — use on surface/card background (e.g. inside make_centered_card)
def CardTitleLabel(parent, text, **kwargs):
    """Page/screen title on card."""
    return ttk.Label(parent, text=text, style="Card.Title.TLabel", **kwargs)


def CardHeadingLabel(parent, text, **kwargs):
    """Section heading on card."""
    return ttk.Label(parent, text=text, style="Card.Heading.TLabel", **kwargs)


def CardSubheadingLabel(parent, text, **kwargs):
    """Subsection or card title on card."""
    return ttk.Label(parent, text=text, style="Card.Subheading.TLabel", **kwargs)


def CardCaptionLabel(parent, text, **kwargs):
    """Secondary/muted text on card."""
    return ttk.Label(parent, text=text, style="Card.Caption.TLabel", **kwargs)
