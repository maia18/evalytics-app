import flet as ft

from components.core.constants.constants import (
    CARD,
    BORDA,
    TEXTO_PRINCIPAL,
    TEXTO_SECUNDARIO,
)


def criar_stats_card(
    titulo: str,
    valor: str,
    cores: dict[str, str],
) -> ft.Container:
    """
    Renderiza um cartão de métrica utilizando os tokens
    do Design System para funcionar em Light e Dark Mode.
    """

    return ft.Container(
        expand=1,
        padding=15,
        border_radius=8,
        bgcolor=cores[CARD],
        border=ft.Border.all(
            1,
            cores[BORDA],
        ),
        content=ft.Column(
            spacing=5,
            controls=[
                ft.Text(
                    titulo,
                    size=12,
                    color=cores[TEXTO_SECUNDARIO],
                ),
                ft.Text(
                    str(valor),
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=cores[TEXTO_PRINCIPAL],
                ),
            ],
        ),
    )