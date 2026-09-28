import flet as ft

from components.core.constants.constants import COR_TEXTO_TITULO


def criar_logo() -> ft.Row:
    """
    Cria o componente de identidade visual da aplicação.
    """

    return ft.Row(
        spacing=10,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            # Logo da plataforma
            ft.Image(
                src="imgs/logo.png",
                width=38,
                height=38,
                fit="CONTAIN",
            ),

            # Nome da aplicação
            ft.Text(
                "Evalytics",
                size=20,
                weight=ft.FontWeight.BOLD,
                color=COR_TEXTO_TITULO,
            ),
        ],
    )