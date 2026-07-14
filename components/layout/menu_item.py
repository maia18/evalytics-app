# ==========================================
# components/layout/menu_item.py
# Componente reutilizável do menu lateral
# ==========================================

import flet as ft

from components.theme.theme import AppTheme
from components.layout.menu import MenuItemData


class MenuItem(ft.Container):
    """
    Item reutilizável do menu lateral.

    O mesmo componente funciona para:
        • Sidebar expandida
        • Sidebar colapsada
    """

    def __init__(
        self,
        item: MenuItemData,
        theme: AppTheme,
        collapsed: bool,
        on_click,
    ):

        self.item = item
        self.theme = theme
        self.collapsed = collapsed
        self.on_click = on_click

        super().__init__(
            height=48,
            border_radius=theme.radius.MD,
            content=self._build(),
        )

    def _build(self):

        return ft.TextButton(

            expand=True,

            style=ft.ButtonStyle(

                padding=self.theme.spacing.MD,

                shape=ft.RoundedRectangleBorder(
                    radius=self.theme.radius.MD
                ),

                overlay_color=self.theme.colors.border,

            ),

            on_click=lambda _: self.on_click(self.item.route),

            content=self._content(),
        )

    def _content(self):

        icon = ft.Icon(

            self.item.icon,

            size=20,

            color=self.theme.colors.text,

        )

        # Sidebar colapsada
        if self.collapsed:

            return ft.Container(

                alignment=ft.alignment.center,

                content=ft.Tooltip(

                    message=self.item.title,

                    content=icon,

                )

            )

        # Sidebar expandida
        return ft.Row(

            spacing=self.theme.spacing.MD,

            vertical_alignment=ft.CrossAxisAlignment.CENTER,

            controls=[

                icon,

                ft.Text(

                    self.item.title,

                    size=self.theme.typography.size.MD,

                    weight=self.theme.typography.weight.MEDIUM,

                    color=self.theme.colors.text,

                )

            ],

        )