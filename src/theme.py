"""Centralized theme definitions for Dark and Light modes."""

DARK = {
    "bg": "#09090B",
    "bg_secondary": "#18181B",
    "bg_card_start": "#18181B",
    "bg_card_end": "#27272A",
    "border": "#3F3F46",
    "text": "#FAFAFA",
    "text_secondary": "#A1A1AA",
    "text_muted": "#71717A",
    "accent": "#06B6D4",
    "accent_dark_text": "#09090B",
    "sidebar_hover": "#27272A",
    # Plotly chart colors
    "plot_bg": "#09090B",
    "plot_paper_bg": "#09090B",
    "plot_grid": "#27272A",
    "plot_font_color": "#FAFAFA",
}

LIGHT = {
    "bg": "#FFFFFF",
    "bg_secondary": "#F4F4F5",
    "bg_card_start": "#F4F4F5",
    "bg_card_end": "#E4E4E7",
    "border": "#D4D4D8",
    "text": "#18181B",
    "text_secondary": "#52525B",
    "text_muted": "#71717A",
    "accent": "#0891B2",
    "accent_dark_text": "#FFFFFF",
    "sidebar_hover": "#E4E4E7",
    # Plotly chart colors
    "plot_bg": "#FFFFFF",
    "plot_paper_bg": "#FFFFFF",
    "plot_grid": "#E4E4E7",
    "plot_font_color": "#18181B",
}


def get_theme(mode: str = "dark") -> dict:
    """Return the color palette for the given mode ('dark' or 'light')."""
    return LIGHT if mode == "light" else DARK
