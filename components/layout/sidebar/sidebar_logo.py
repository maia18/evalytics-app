import flet as ft
from components.core.theme.theme import AppColors

def criar_logo(cores, compact=False):
    
    """Cria logo da sidebar"""
    
    if compact:
        return ft.Container(
            content=ft.Icon(ft.Icons.ANALYTICS, color=AppColors.PRIMARIA, size=28),
            padding=8,
            alignment=ft.Alignment.CENTER,
        )
    else:
        return ft.Container(
            content=ft.Row(
                spacing=10,
                controls=[
                    ft.Icon(ft.Icons.ANALYTICS, color=AppColors.PRIMARIA, size=28),
                    ft.Text("Evalytics", size=18, weight="bold", color=cores["TEXTO_PRINCIPAL"]),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=15,
            height=60,
        )
