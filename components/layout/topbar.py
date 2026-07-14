# ==========================================
# components/layout/topbar.py
# Barra superior reutilizável
# ==========================================

import flet as ft

from components.theme.theme import AppTheme
from utils.services.location_service import obter_localizacao


class TopBar(ft.Container):
    """
    Barra superior da aplicação.

    Responsável por exibir:

    • Menu Hambúrguer
    • Título
    • Subtítulo
    • Localização
    • Alternância de Tema
    • Notificações
    • Avatar
    """

    def __init__(
        self,
        page: ft.Page,
        theme: AppTheme,
        title: str,
        subtitle: str = "",
        dark_mode: bool = False,
        on_menu=None,
        on_toggle_theme=None,
        show_menu=True,
    ):

        self.page = page
        self.theme = theme
        self.dark_mode = dark_mode
        self.on_menu = on_menu
        self.on_toggle_theme = on_toggle_theme

        self.location = obter_localizacao()

        super().__init__(

            bgcolor=theme.colors.card,

            padding=theme.spacing.XL,

            border=ft.Border(
                bottom=ft.BorderSide(
                    1,
                    theme.colors.border
                )
            ),

            content=self._build(
                title,
                subtitle,
                show_menu,
            ),
        )

    # ------------------------------------

    def _build(
        self,
        title,
        subtitle,
        show_menu,
    ):

        return ft.Row(

            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

            vertical_alignment=ft.CrossAxisAlignment.CENTER,

            controls=[

                self._left_section(
                    title,
                    subtitle,
                    show_menu,
                ),

                self._right_section(),

            ],
        )

    # ------------------------------------

    def _left_section(
        self,
        title,
        subtitle,
        show_menu,
    ):

        controls = []

        if show_menu:

            controls.append(

                ft.IconButton(

                    icon=ft.Icons.MENU,

                    on_click=self.on_menu,

                )

            )

        controls.append(

            ft.Column(

                spacing=2,

                controls=[

                    ft.Text(

                        title,

                        size=self.theme.typography.size.XL,

                        weight=self.theme.typography.weight.BOLD,

                        color=self.theme.colors.text,

                    ),

                    ft.Text(

                        subtitle,

                        size=self.theme.typography.size.SM,

                        color=self.theme.colors.text_secondary,

                    )

                ]

            )

        )

        return ft.Row(
            spacing=self.theme.spacing.MD,
            controls=controls,
        )

    # ------------------------------------

    def _right_section(self):

        return ft.Row(

            spacing=self.theme.spacing.MD,

            vertical_alignment=ft.CrossAxisAlignment.CENTER,

            controls=[

                self._location(),

                self._theme_button(),

                self._notifications(),

                self._avatar(),

            ],

        )

    # ------------------------------------

    def _location(self):

        return ft.Container(

            padding=self.theme.spacing.MD,

            border_radius=self.theme.radius.MD,

            bgcolor=self.theme.colors.background,

            content=ft.Row(

                spacing=self.theme.spacing.SM,

                controls=[

                    ft.Icon(

                        ft.Icons.LOCATION_ON_OUTLINED,

                        size=18,

                        color=self.theme.colors.primary,

                    ),

                    ft.Text(

                        self.location,

                        size=self.theme.typography.size.SM,

                        color=self.theme.colors.text,

                    )

                ]

            ),

        )

    # ------------------------------------

    def _theme_button(self):

        return ft.IconButton(

            icon=(
                ft.Icons.LIGHT_MODE_OUTLINED
                if self.dark_mode
                else ft.Icons.DARK_MODE_OUTLINED
            ),

            tooltip="Alternar tema",

            on_click=self.on_toggle_theme,

        )

    # ------------------------------------

    def _notifications(self):

        return ft.IconButton(

            icon=ft.Icons.NOTIFICATIONS_NONE,

            tooltip="Notificações",

        )

    # ------------------------------------

    def _avatar(self):

        return ft.CircleAvatar(

            radius=18,

            bgcolor=self.theme.colors.primary,

            content=ft.Text(

                "AC",

                color="white",

                weight=self.theme.typography.weight.BOLD,

            ),

        )