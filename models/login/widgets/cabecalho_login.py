import flet as ft

def criar_cabecalho(COR_TEXTO_TITULO, COR_TEXTO_SECUNDARIO):
    return ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
        controls=[
            ft.Container(
                content=ft.Image(src="imgs/logo.png", width=60, height=60, fit="CONTAIN")
            ),
            ft.Text("Bem-vindo ao Evalytics", size=28, weight="bold", color=COR_TEXTO_TITULO),
            ft.Text(
                "Faça login para gerenciar as avaliações institucionais.",
                size=16,
                color=COR_TEXTO_SECUNDARIO,
                text_align=ft.TextAlign.CENTER
            )
        ]
    )
