import flet as ft

from models.login.core.cabecalho_login import criar_cabecalho
from models.login.widgets.campos_login import criar_campo_nome, criar_campo_email, criar_campo_senha
from models.login.widgets.extras_login import criar_opcoes_extras
from models.login.widgets.card_login import criar_card_login
from models.login.widgets.social_login import criar_login_social
from models.login.core.rodape import criar_rodape_termos
from models.login.core.logica_abas import obter_funcao_alternar

from components.core.constants.constants import *

def ViewLogin(page: ft.Page, mudar_tela):

    def fazer_login(e):
        mudar_tela("/inicio")

    cabecalho = criar_cabecalho(COR_TEXTO_TITULO, COR_TEXTO_SECUNDARIO)
    campo_nome = criar_campo_nome(COR_TEXTO_TITULO, COR_TEXTO_SECUNDARIO, COR_BORDA)
    campo_email = criar_campo_email(COR_TEXTO_TITULO, COR_TEXTO_SECUNDARIO, COR_BORDA)
    campo_senha = criar_campo_senha(COR_TEXTO_TITULO, COR_TEXTO_SECUNDARIO, COR_BORDA)
    opcoes_extras = criar_opcoes_extras(COR_TEXTO_SECUNDARIO, COR_PRIMARIA)

    btn_login = ft.ElevatedButton(
        "Sign In",
        bgcolor=COR_PRIMARIA,
        color="white",
        width=float("inf"),
        height=45,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        on_click=fazer_login
    )
    
    secao_social = criar_login_social(COR_TEXTO_SECUNDARIO, COR_BORDA)
    rodape_termos = criar_rodape_termos(COR_TEXTO_SECUNDARIO, COR_PRIMARIA)

    estilo_aba = ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=0),
        color=COR_TEXTO_TITULO,
        bgcolor=COR_CARD 
    )
    
    btn_aba_signin = ft.OutlinedButton("Sign In", data="signin", style=estilo_aba)
    btn_aba_signin.style.side = ft.border.BorderSide(1, COR_PRIMARIA)
    
    btn_aba_signup = ft.OutlinedButton("Sign Up", data="signup", style=estilo_aba)
    btn_aba_signup.style.side = ft.border.BorderSide(1, "transparent")
    
    funcao_alternar = obter_funcao_alternar(
        btn_aba_signin, btn_aba_signup, campo_nome, opcoes_extras, 
        btn_login, COR_TEXTO_TITULO, COR_CARD, COR_PRIMARIA
    )
    
    btn_aba_signin.on_click = funcao_alternar
    btn_aba_signup.on_click = funcao_alternar
    
    cabecalho_abas = ft.Row([btn_aba_signin, btn_aba_signup], alignment=ft.MainAxisAlignment.CENTER, spacing=0)
    
    card_login = criar_card_login(
        cabecalho_abas, 
        campo_nome, 
        campo_email, 
        campo_senha, 
        opcoes_extras, 
        btn_login, 
        secao_social, 
        COR_CARD
    )
        
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