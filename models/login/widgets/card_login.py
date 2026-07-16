import flet as ft

def criar_card_login(campo_email, campo_senha, opcoes_extras, btn_login, secao_social, COR_CARD):
    return ft.Container(
        width=420,
        bgcolor=COR_CARD,
        padding=40,
        border_radius=12,
        shadow=ft.BoxShadow(blur_radius=15, color="black12"),
        content=ft.Column(
            spacing=20,
            controls=[campo_email, campo_senha, opcoes_extras, btn_login, secao_social]
        )
    )
