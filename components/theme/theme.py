# ==========================================
# components/theme/theme.py
# Tema principal da aplicação
# ==========================================

from dataclasses import dataclass

from .colors import LIGHT_COLORS, DARK_COLORS
from .spacing import spacing
from .radius import radius
from .typography import typography


@dataclass(frozen=True)
class AppTheme:
    """
    Tema completo da aplicação.

    Reúne todas as configurações visuais em um único objeto.
    """

    colors: object
    spacing: object
    radius: object
    typography: object


LIGHT_THEME = AppTheme(
    colors=LIGHT_COLORS,
    spacing=spacing,
    radius=radius,
    typography=typography,
)


DARK_THEME = AppTheme(
    colors=DARK_COLORS,
    spacing=spacing,
    radius=radius,
    typography=typography,
)


def get_theme(dark_mode: bool) -> AppTheme:
    """
    Retorna o tema de acordo com o modo atual.
    """

    return DARK_THEME if dark_mode else LIGHT_THEME