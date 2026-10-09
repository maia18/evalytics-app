import flet as ft
from typing import Callable
from components.core.constants.constants import (
    COR_PRIMARIA,
)

def criar_cta(
    mudar_tela: Callable[[str], None],
) -> ft.Container:
    """Cria a seção final de chamada para ação da Landing Page."""

    return ft.Container(
        margin=ft.Margin.symmetric(
            horizontal=40,
            vertical=45,
        ),
        padding=ft.Padding.symmetric(
            horizontal=45,
            vertical=38,
        ),
        bgcolor=COR_PRIMARIA,
        border_radius=18,
        content=ft.ResponsiveRow(
            columns=12,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            run_spacing=24,
            controls=[
                # =====================================================
                # TEXTO
                # =====================================================

                ft.Container(
                    col={
                        "xs": 12,
                        "sm": 12,
                        "md": 8,
                        "lg": 8,
                        "xl": 8,
                    },
                    content=ft.Column(
                        spacing=8,
                        controls=[
                            ft.Text(
                                "Pronto para começar?",
                                size=26,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.WHITE,
                            ),

                            ft.Text(
                                "Acesse o Evalytics e acompanhe "
                                "as avaliações da sua instituição.",
                                size=14,
                                color=ft.Colors.WHITE70,
                            ),
                        ],
                    ),
                ),

                # =====================================================
                # BOTÃO
                # =====================================================

                ft.Container(
                    col={
                        "xs": 12,
                        "sm": 12,
                        "md": 4,
                        "lg": 4,
                        "xl": 4,
                    },
                    alignment=ft.Alignment.CENTER_RIGHT,
                    content=ft.ElevatedButton(
                        "Entrar na plataforma",
                        height=46,
                        bgcolor=ft.Colors.WHITE,
                        color=COR_PRIMARIA,
                        on_click=lambda e: mudar_tela("/login"),
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(
                                radius=8,
                            ),
                            padding=ft.Padding.symmetric(
                                horizontal=24,
                            ),
                        ),
                    ),
                ),
            ],
        ),
    )