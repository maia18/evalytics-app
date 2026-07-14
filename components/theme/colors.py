# ==========================================
# components/theme/colors.py
# Centralização de todas as cores do sistema
# ==========================================

from dataclasses import dataclass


@dataclass(frozen=True)
class ColorPalette:
    """Paleta de cores da aplicação."""

    background: str
    card: str
    border: str

    text: str
    text_secondary: str

    primary: str
    primary_hover: str

    success: str
    warning: str
    danger: str

    overlay: str


# ---------- Tema Claro ----------

LIGHT_COLORS = ColorPalette(

    background="#F9FAFB",

    card="#FFFFFF",

    border="#E5E7EB",

    text="#111827",

    text_secondary="#6B7280",

    primary="#F59E0B",

    primary_hover="#D97706",

    success="#10B981",

    warning="#F59E0B",

    danger="#EF4444",

    overlay="#00000088",

)


# ---------- Tema Escuro ----------

DARK_COLORS = ColorPalette(

    background="#1E1E1E",

    card="#2C2C2C",

    border="#3C3C3C",

    text="#FFFFFF",

    text_secondary="#CFCFCF",

    primary="#F59E0B",

    primary_hover="#D97706",

    success="#10B981",

    warning="#FBBF24",

    danger="#F87171",

    overlay="#00000088",

)