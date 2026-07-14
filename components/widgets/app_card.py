# ==========================================
# components/widgets/app_card.py
# Card padrão do sistema
# ==========================================

import flet as ft

from components.theme.theme import AppTheme


class AppCard(ft.Container):

    """
    Card padrão utilizado em toda a aplicação.
    """

    def __init__(
        self,
        theme: AppTheme,
        content,
        padding=None,
        expand=False,
        width=None,
        height=None,
        on_click=None,
    ):

        super().__init__(

            content=content,

            expand=expand,

            width=width,

            height=height,

            padding=padding or theme.spacing.XL,

            bgcolor=theme.colors.card,

            border_radius=theme.radius.LG,

            border=ft.Border.all(
                1,
                theme.colors.border,
            ),

            animate=200,

            on_click=on_click,

        )