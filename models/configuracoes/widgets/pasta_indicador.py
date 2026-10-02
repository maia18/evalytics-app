import flet as ft

from typing import Callable

from components.core.constants.constants import (
    CARD_SECUNDARIO,
    BORDA,
    TEXTO_PRINCIPAL,
    TEXTO_SECUNDARIO,
    COR_PRIMARIA,
)

def criar_pasta_indicador(
    titulo: str,
    qtd: int,
    abrir_pasta: Callable[[str], None],
    cores: dict[str, str],
) -> ft.Container:
    """
    Cria um card clicável representando um eixo de avaliação.
    """

    return ft.Container(
        bgcolor=cores[CARD_SECUNDARIO],
        border=ft.Border(
            top=ft.BorderSide(1, cores[BORDA]),
            bottom=ft.BorderSide(1, cores[BORDA]),
            left=ft.BorderSide(1, cores[BORDA]),
            right=ft.BorderSide(1, cores[BORDA]),
        ),
        border_radius=8,
        padding=20,
        ink=True,
        on_click=lambda e: abrir_pasta(titulo),

        content=ft.Row(
            spacing=15,
            controls=[
                ft.Icon(
                    ft.Icons.FOLDER,
                    color=cores[COR_PRIMARIA],
                    size=28,
                ),

                ft.Column(
                    spacing=2,
                    controls=[
                        ft.Text(
                            titulo,
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=cores[TEXTO_PRINCIPAL],
                        ),

                        ft.Text(
                            f"{qtd} indicadores",
                            size=13,
                            color=cores[TEXTO_SECUNDARIO],
                        ),
                    ],
                ),
            ],
        ),
    )