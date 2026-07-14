# ==========================================
# components/theme/typography.py
# Tipografia padronizada da aplicação
# ==========================================

from dataclasses import dataclass
import flet as ft


@dataclass(frozen=True)
class FontSize:
    """Tamanhos de fonte."""

    XS: int = 10
    SM: int = 12
    MD: int = 14
    LG: int = 16
    XL: int = 20
    XXL: int = 24
    DISPLAY: int = 32


@dataclass(frozen=True)
class FontWeight:
    """Pesos das fontes."""

    LIGHT = ft.FontWeight.W_300
    NORMAL = ft.FontWeight.W_400
    MEDIUM = ft.FontWeight.W_500
    SEMIBOLD = ft.FontWeight.W_600
    BOLD = ft.FontWeight.W_700


class Typography:
    """Estilos tipográficos reutilizáveis."""

    size = FontSize()
    weight = FontWeight()


typography = Typography()