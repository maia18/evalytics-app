# ==========================================
# components/theme/spacing.py
# Espaçamentos padronizados do sistema
# ==========================================

from dataclasses import dataclass


@dataclass(frozen=True)
class Spacing:
    """Espaçamentos padrão da aplicação."""

    NONE: int = 0

    XS: int = 4
    SM: int = 8
    MD: int = 12
    LG: int = 16
    XL: int = 20
    XXL: int = 24
    XXXL: int = 32


spacing = Spacing()