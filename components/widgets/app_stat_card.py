# ==========================================
# components/widgets/app_stat_card.py
# Card de indicadores
# ==========================================

import flet as ft

from components.widgets.app_card import AppCard
from components.theme.theme import AppTheme


class AppStatCard(AppCard):
    """
    Card para exibição de indicadores.

    Exemplo:

        Cursos
        12
        ↑ +8%
    """

    def __init__(
        self,
        theme: AppTheme,
        title: str,
        value,
        icon,
        subtitle: str = "",
        color: str = None,
        width=None,
        expand=True,
    ):

        color = color or theme.colors.primary

        super().__init__(

            theme=theme,

            width=width,

            expand=expand,

            content=self._content(
                theme,
                title,
                value,
                icon,
                subtitle,
                color,
            ),
        )

    # -----------------------------------------

    def _content(
        self,
        theme,
        title,
        value,
        icon,
        subtitle,
        color,
    ):

        return ft.Column(

            spacing=theme.spacing.MD,

            controls=[

                ft.Row(

                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

                    controls=[

                        ft.Text(

                            title,

                            size=theme.typography.size.SM,

                            color=theme.colors.text_secondary,

                        ),

                        ft.Icon(

                            icon,

                            color=color,

                            size=24,

                        ),

                    ],

                ),

                ft.Text(

                    str(value),

                    size=theme.typography.size.XXL,

                    weight=theme.typography.weight.BOLD,

                    color=theme.colors.text,

                ),

                ft.Text(

                    subtitle,

                    size=theme.typography.size.SM,

                    color=theme.colors.text_secondary,

                ),

            ],

        )