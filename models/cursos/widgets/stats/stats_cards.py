import flet as ft

def criar_stats_card(titulo, valor, cor_texto):
    return ft.Container(
        expand=1,
        padding=15,
        border_radius=8,
        bgcolor="white",
        content=ft.Column(
            spacing=5,
            controls=[
                ft.Text(titulo, size=12, color="grey"),
                ft.Text(str(valor), size=20, weight="bold", color=cor_texto),
            ]
        )
    )
