import flet as ft
from components.landing.palette import TEXTO_CLARO

def criar_logo() -> ft.Row:
    """Cria o componente de identidade visual da aplicação."""

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
                color=TEXTO_CLARO,
            ),
        ],
    )
