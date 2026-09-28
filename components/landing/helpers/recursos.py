import flet as ft

from components.core.constants.constants import (
    COR_TEXTO_TITULO,
    COR_TEXTO_SECUNDARIO,
    COR_PRIMARIA,
    COR_FUNDO,
)


def criar_card_recurso(
    icone,
    titulo: str,
    descricao: str,
) -> ft.Container:

    return ft.Container(
        width=235,
        height=190,
        padding=24,
        bgcolor=COR_FUNDO,
        border_radius=14,
        border=ft.Border.all(
            1,
            ft.Colors.BLACK12,
        ),
        content=ft.Column(
            spacing=14,
            controls=[
                ft.Container(
                    width=42,
                    height=42,
                    border_radius=9,
                    bgcolor=ft.Colors.with_opacity(
                        0.10,
                        COR_PRIMARIA,
                    ),
                    alignment=ft.Alignment.CENTER,
                    content=ft.Icon(
                        icone,
                        size=21,
                        color=COR_PRIMARIA,
                    ),
                ),

                ft.Text(
                    titulo,
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=COR_TEXTO_TITULO,
                ),

                ft.Text(
                    descricao,
                    size=13,
                    color=COR_TEXTO_SECUNDARIO,
                ),
            ],
        ),
    )