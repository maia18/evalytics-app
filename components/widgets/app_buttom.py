# ==========================================
# components/widgets/app_button.py
# Botão padrão do sistema
# ==========================================

import flet as ft

from components.theme.theme import AppTheme


class AppButton(ft.ElevatedButton):

    """
    Botão reutilizável da aplicação.

    Variantes:

    primary
    secondary
    success
    danger
    text
    """

    def __init__(
        self,
        theme: AppTheme,
        text: str,
        on_click=None,
        icon=None,
        variant="primary",
        width=None,
        expand=False,
        disabled=False,
    ):

        colors = self._colors(theme, variant)

        super().__init__(

            text=text,

            icon=icon,

            width=width,

            expand=expand,

            disabled=disabled,

            on_click=on_click,

            style=ft.ButtonStyle(

                bgcolor=colors["bg"],

                color=colors["fg"],

                padding=theme.spacing.LG,

                shape=ft.RoundedRectangleBorder(
                    radius=theme.radius.MD
                ),

            ),

        )

    # -----------------------------------------

    def _colors(self, theme, variant):

        if variant == "danger":

            return {
                "bg": theme.colors.danger,
                "fg": "white",
            }

        if variant == "success":

            return {
                "bg": theme.colors.success,
                "fg": "white",
            }

        if variant == "secondary":

            return {
                "bg": theme.colors.card,
                "fg": theme.colors.text,
            }

        if variant == "text":

            return {
                "bg": None,
                "fg": theme.colors.primary,
            }

        return {
            "bg": theme.colors.primary,
            "fg": "white",
        }