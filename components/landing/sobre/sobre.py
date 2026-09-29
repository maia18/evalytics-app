import flet as ft

from components.landing.sobre.conteudo import criar_sobre_conteudo
from components.landing.sobre.visual import criar_sobre_visual

def criar_secao_sobre() -> ft.Container:

    sobre_conteudo = criar_sobre_conteudo()
    sobre_visual = criar_sobre_visual()

    return ft.Container(
        key=ft.ScrollKey("sobre"),
        padding=ft.Padding.symmetric(
            horizontal=20,
            vertical=75,
        ),
        content=ft.ResponsiveRow(
            columns=12,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            run_spacing=35,
            controls=[
                ft.Container(
                    col={
                        "xs": 12,
                        "sm": 12,
                        "md": 12,
                        "lg": 7,
                        "xl": 7,
                    },
                    padding=ft.Padding.only(
                        right=20,
                    ),
                    content=sobre_conteudo,
                ),

                ft.Container(
                    col={
                        "xs": 12,
                        "sm": 12,
                        "md": 12,
                        "lg": 5,
                        "xl": 5,
                    },
                    alignment=ft.Alignment.CENTER,
                    content=sobre_visual,
                ),
            ],
        ),
    )