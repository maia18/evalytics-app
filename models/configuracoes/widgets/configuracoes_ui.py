import flet as ft
from components.core.constants.constants import CARD

def criar_layout_principal(
    cores_layout: dict,
    menu_abas: ft.Control,
    area_conteudo_aba: ft.Control,
) -> ft.Column:
    """
    Constrói a área principal da página de configurações.
        O cabeçalho da página é fornecido pelo ResponsiveLayout.
    """

    return ft.Column(
        expand=True,
        controls=[
            ft.Container(
                expand=True,
                bgcolor=cores_layout[CARD],
                border_radius=10,
                padding=20,
                shadow=None,
                content=ft.Column(
                    expand=True,
                    controls=[
                        menu_abas,

                        ft.Divider(
                            height=20,
                            color=ft.Colors.TRANSPARENT,
                        ),

                        ft.Container(
                            expand=True,
                            padding=10,
                            content=area_conteudo_aba,
                        ),
                    ],
                ),
            ),
        ],
    )