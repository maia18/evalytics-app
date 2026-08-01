import flet as ft
from typing import Optional
from components.core.constants.constants import (
    CARD,
    PADDING_CARD_PADRAO,
    BORDA_RADIUS_CARD_PADRAO,
    SOMBRA_CARD_PADRAO
)

# Casca visual compartilhada dos cards da aplicação: fundo, padding, borda e sombra padrão.
def criar_card_base(
    cores: dict[str, str],
    content: ft.Control,
    expand: bool = False,
    height: Optional[int] = None,
) -> ft.Container:
    return ft.Container(
        bgcolor=cores[CARD],
        padding=PADDING_CARD_PADRAO,
        border_radius=BORDA_RADIUS_CARD_PADRAO,
        shadow=SOMBRA_CARD_PADRAO,
        expand=expand,
        height=height,
        content=content, # O conteúdo real (gráficos, tabelas, textos) é injetado dinamicamente aqui dentro
    )