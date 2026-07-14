# ==========================================
# components/theme/radius.py
# Raios de borda padronizados
# ==========================================

from dataclasses import dataclass


@dataclass(frozen=True)
class Radius:
    """Raios padrão da aplicação."""

    NONE: int = 0

    XS: int = 4
    SM: int = 6
    MD: int = 8
    LG: int = 12
    XL: int = 16
    XXL: int = 20

    CIRCLE: int = 999


radius = Radius()