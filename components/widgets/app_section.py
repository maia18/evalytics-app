# ==========================================
# components/widgets/app_section.py
# Seção reutilizável
# ==========================================

import flet as ft

from components.theme.theme import AppTheme


class AppSection(ft.Column):
    """
    Seção reutilizável da aplicação.

    Exemplo:

    Dashboard
    Informações gerais

    [conteúdo]
    """

    def __init__(
        self,
        theme: AppTheme,
        title: str,
        content,
        subtitle: str = "",
        actions=None,
    ):

        super().__init__(

            spacing=theme.spacing.LG,

            controls=[

                self._header(
                    theme,
                    title,
                    subtitle,
                    actions,
                ),

                content,

            ]

        )

    # ----------------------------------

    def _header(
        self,
        theme,
        title,
        subtitle,
        actions,
    ):

        return ft.Row(

            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

            vertical_alignment=ft.CrossAxisAlignment.CENTER,

            controls=[

                ft.Column(

                    spacing=2,

                    controls=[

                        ft.Text(

                            title,

                            size=theme.typography.size.XL,

                            weight=theme.typography.weight.BOLD,

                            color=theme.colors.text,

                        ),

                        ft.Text(

                            subtitle,

                            size=theme.typography.size.SM,

                            color=theme.colors.text_secondary,

                        ),

                    ],

                ),

                actions if actions else ft.Container(),

            ],

        )