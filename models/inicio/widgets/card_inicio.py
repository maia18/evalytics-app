import flet as ft
# from components.core.theme.theme import AppColors
from components.core.constants import *

def criar_card(layout, titulo, descricao, icone, rota, mudar_tela):
    return ft.Container(
        width=300,
        bgcolor=layout.cores["CARD"],
        padding=20,
        border_radius=12,
        border=ft.Border(
            left=ft.BorderSide(width=1, color=layout.cores["BORDA"]),
            top=ft.BorderSide(width=1, color=layout.cores["BORDA"]),
            right=ft.BorderSide(width=1, color=layout.cores["BORDA"]),
            bottom=ft.BorderSide(width=1, color=layout.cores["BORDA"]),
        ),
        ink=True,
        on_click=lambda e: mudar_tela(rota),
        content=ft.Column([
            ft.Icon(icone, color=COR_PRIMARIA, size=30),
            ft.Text(titulo, weight="bold", color=layout.cores["TEXTO_PRINCIPAL"]),
            ft.Text(descricao, size=12, color="grey")
        ])
    )
