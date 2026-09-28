import flet as ft

from components.core.constants.constants import (
    COR_TEXTO_TITULO,
    COR_TEXTO_SECUNDARIO,
    COR_PRIMARIA,
    COR_FUNDO,
)


def criar_etapa(
    numero: str,
    titulo: str,
    descricao: str,
) -> ft.Row:

    return ft.Row(
        spacing=15,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Container(
                width=38,
                height=38,
                border_radius=8,
                bgcolor=ft.Colors.with_opacity(
                    0.10,
                    COR_PRIMARIA,
                ),
                alignment=ft.Alignment.CENTER,
                content=ft.Text(
                    numero,
                    size=12,
                    weight=ft.FontWeight.BOLD,
                    color=COR_PRIMARIA,
                ),
            ),

            ft.Column(
                spacing=2,
                expand=True,
                controls=[
                    ft.Text(
                        titulo,
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=COR_TEXTO_TITULO,
                    ),

                    ft.Text(
                        descricao,
                        size=12,
                        color=COR_TEXTO_SECUNDARIO,
                    ),
                ],
            ),
        ],
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


def criar_indicador(
    titulo: str,
    valor: str,
) -> ft.Container:

    return ft.Container(
        expand=True,
        padding=15,
        bgcolor=ft.Colors.with_opacity(
            0.06,
            COR_PRIMARIA,
        ),
        border_radius=10,
        content=ft.Column(
            spacing=5,
            controls=[
                ft.Text(
                    titulo,
                    size=12,
                    color=COR_TEXTO_SECUNDARIO,
                ),

                ft.Text(
                    valor,
                    size=26,
                    weight=ft.FontWeight.BOLD,
                    color=COR_PRIMARIA,
                ),
            ],
        ),
    )