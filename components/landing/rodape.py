import flet as ft

from components.core.constants.constants import (
    COR_TEXTO_TITULO,
    COR_TEXTO_SECUNDARIO,
)


def criar_rodape() -> ft.Container:

    return ft.Container(
        padding=ft.Padding.symmetric(
            horizontal=20,
            vertical=25,
        ),
        border=ft.Border(
            top=ft.BorderSide(
                1,
                ft.Colors.BLACK12,
            ),
        ),
        content=ft.ResponsiveRow(
            columns=12,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            run_spacing=8,
            controls=[
                ft.Container(
                    col={
                        "xs": 12,
                        "sm": 12,
                        "md": 4,
                        "lg": 4,
                        "xl": 4,
                    },
                    alignment=ft.Alignment.CENTER_LEFT,
                    content=ft.Text(
                        "Evalytics",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=COR_TEXTO_TITULO,
                    ),
                ),

                ft.Container(
                    col={
                        "xs": 12,
                        "sm": 12,
                        "md": 4,
                        "lg": 4,
                        "xl": 4,
                    },
                    alignment=ft.Alignment.CENTER,
                    content=ft.Text(
                        "Avaliação institucional orientada por dados",
                        size=12,
                        color=COR_TEXTO_SECUNDARIO,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ),

                ft.Container(
                    col={
                        "xs": 12,
                        "sm": 12,
                        "md": 4,
                        "lg": 4,
                        "xl": 4,
                    },
                    alignment=ft.Alignment.CENTER_RIGHT,
                    content=ft.Text(
                        "© 2026 Evalytics",
                        size=12,
                        color=COR_TEXTO_SECUNDARIO,
                    ),
                ),
            ],
        ),
    )