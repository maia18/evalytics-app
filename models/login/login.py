import flet as ft

from models.login.widgets.cabecalho_login import criar_cabecalho
from models.login.widgets.campos_login import criar_campo_email, criar_campo_senha
from models.login.widgets.extras_login import criar_opcoes_extras
from models.login.widgets.card_login import criar_card_login
from models.login.widgets.social_login import criar_login_social
from models.login.widgets.rodape import criar_rodape_termos

from components.core.constants import *

def ViewLogin(page: ft.Page, mudar_tela):

    def fazer_login(e):
        mudar_tela("/inicio")

    # Componentes
    cabecalho = criar_cabecalho(COR_TEXTO_TITULO, COR_TEXTO_SECUNDARIO)
    campo_email = criar_campo_email(COR_TEXTO_TITULO, COR_TEXTO_SECUNDARIO, COR_BORDA)
    campo_senha = criar_campo_senha(COR_TEXTO_TITULO, COR_TEXTO_SECUNDARIO, COR_BORDA)
    opcoes_extras = criar_opcoes_extras(COR_TEXTO_SECUNDARIO, COR_PRIMARIA)

    btn_login = ft.ElevatedButton(
        "Entrar",
        bgcolor=COR_PRIMARIA,
        color="white",
        width=float("inf"),
        height=45,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        on_click=fazer_login
    )
    
    secao_social = criar_login_social(COR_TEXTO_SECUNDARIO, COR_BORDA)
    card_login = criar_card_login(campo_email, campo_senha, opcoes_extras, btn_login, secao_social, COR_CARD)
    rodape_termos = criar_rodape_termos(COR_TEXTO_SECUNDARIO, COR_PRIMARIA)
    
    return ft.View(
        route="/",
        bgcolor=COR_FUNDO,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        padding=20,
        controls=[
            ft.Container(
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=30,
                    controls=[cabecalho, card_login, rodape_termos]
                )
            )
        ]
    )
