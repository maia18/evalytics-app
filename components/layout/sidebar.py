# ==========================================
# components/layout/sidebar.py
# Sidebar reutilizável
# ==========================================

import flet as ft

from components.layout.menu import (
    MENU_ITEMS,
    SETTINGS_ITEM,
)

from components.layout.menu_item import MenuItem

from components.theme.theme import AppTheme


class Sidebar(ft.Container):
    """
    Sidebar reutilizável.

    Pode funcionar nos modos:

        • Desktop
        • Tablet (colapsada)
        • Mobile

    Apenas alterando o parâmetro 'collapsed'.
    """

    def __init__(
        self,
        theme: AppTheme,
        collapsed: bool,
        on_navigate,
        current_route: str = "",
    ):

        self.theme = theme
        self.collapsed = collapsed
        self.on_navigate = on_navigate
        self.current_route = current_route

        super().__init__(

            bgcolor=theme.colors.card,

            padding=theme.spacing.XL,

            border=ft.Border(
                right=ft.BorderSide(
                    1,
                    theme.colors.border,
                )
            ),

            content=self._build(),
        )

    # ----------------------------------------

    def _build(self):

        return ft.Column(

            expand=True,

            spacing=0,

            controls=[

                self._logo(),

                ft.Divider(),

                *self._menu_items(),

                ft.Container(expand=True),

                ft.Divider(),

                self._settings(),

            ],

        )

    # ----------------------------------------

    def _logo(self):

        if self.collapsed:

            return ft.Container(

                alignment=ft.alignment.center,

                padding=self.theme.spacing.SM,

                content=ft.Icon(

                    ft.Icons.ANALYTICS,

                    size=30,

                    color=self.theme.colors.primary,

                ),

            )

        return ft.Row(

            spacing=self.theme.spacing.MD,

            controls=[

                ft.Icon(

                    ft.Icons.ANALYTICS,

                    size=28,

                    color=self.theme.colors.primary,

                ),

                ft.Text(

                    "Evalytics",

                    size=self.theme.typography.size.LG,

                    weight=self.theme.typography.weight.BOLD,

                    color=self.theme.colors.text,

                ),

            ],

        )

    # ----------------------------------------

    def _menu_items(self):

        controls = []

        for item in MENU_ITEMS:

            controls.append(

                MenuItem(

                    item=item,

                    theme=self.theme,

                    collapsed=self.collapsed,

                    selected=item.route == self.current_route,

                    on_click=self.on_navigate,

                )

            )

        return controls

    # ----------------------------------------

    def _settings(self):

        return MenuItem(

            item=SETTINGS_ITEM,

            theme=self.theme,

            collapsed=self.collapsed,

            selected=SETTINGS_ITEM.route == self.current_route,

            on_click=self.on_navigate,

        )