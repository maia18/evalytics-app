from typing import Callable
import requests
import flet as ft

from models.login.core.logica_abas import obter_funcao_alternar
from models.login.core.cabecalho_login import criar_cabecalho
from models.login.core.tab_style import criar_estilo_aba
from models.login.core.rodape import criar_rodape_termos
from models.login.widgets.campos_login import (
    criar_campo_nome, 
    criar_campo_email, 
    criar_campo_senha,
)
from models.login.widgets.card_login import criar_card_login
from models.login.widgets.social_login import criar_login_social
from models.login.widgets.extras_login import criar_opcoes_extras

from components.core.constants.constants import (
    COR_TEXTO_TITULO, 
    COR_TEXTO_SECUNDARIO, 
    COR_BORDA, 
    COR_PRIMARIA, 
    COR_CARD, 
    COR_FUNDO,
)

def ViewLogin(page: ft.Page, mudar_tela: Callable[[str], None]) -> ft.View:
    
    FIREBASE_API_KEY = "AIzaSyAqGHhj3-BihICWHvD70smkjcbP2D8Sxnk"

    campo_nome = criar_campo_nome(COR_TEXTO_TITULO, COR_TEXTO_SECUNDARIO, COR_BORDA)
    campo_email = criar_campo_email(COR_TEXTO_TITULO, COR_TEXTO_SECUNDARIO, COR_BORDA)
    campo_senha = criar_campo_senha(COR_TEXTO_TITULO, COR_TEXTO_SECUNDARIO, COR_BORDA)
    opcoes_extras = criar_opcoes_extras(COR_TEXTO_SECUNDARIO, COR_PRIMARIA)

    # === Lógica de Abas para Alternar entre Login e Cadastro ===
    btn_aba_signin = ft.TextButton(
        "Entrar", data="signin", expand=True,
        style=criar_estilo_aba(ativo=True, cor_primaria=COR_PRIMARIA, cor_texto_inativo=COR_TEXTO_TITULO),
    )
    btn_aba_signup = ft.TextButton(
        "Cadastrar-se", data="signup", expand=True,
        style=criar_estilo_aba(ativo=False, cor_primaria=COR_PRIMARIA, cor_texto_inativo=COR_TEXTO_SECUNDARIO),
    )

    def fazer_login(e: ft.ControlEvent) -> None:
       # Acessa o TextField que está na segunda posição (índice 1) da Column
        email = campo_email.controls[1].value.strip()
        senha = campo_senha.controls[1].value.strip()
        if not email or not senha:
            page.open(ft.SnackBar(ft.Text("Preencha e-mail e senha!"), bgcolor=ft.Colors.RED_400))
            return

        # Descobre se está na aba de Cadastro ou Entrar pelo estado do botão
        is_signup = btn_aba_signup.style.color == COR_PRIMARIA if hasattr(btn_aba_signup.style, 'color') else False
        
        # URL da API REST do Firebase Auth
        if is_signup:
            url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_API_KEY}"
        else:
            url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"

        payload = {
            "email": email,
            "password": senha,
            "returnSecureToken": True
        }

        try:
            response = requests.post(url, json=payload)
            data = response.json()

            if response.status_code == 200:
                sucesso = ft.SnackBar(ft.Text("Autenticação realizada com sucesso!"), bgcolor=ft.Colors.GREEN_400)
                page.overlay.append(sucesso)
                sucesso.open = True
                page.update()
                mudar_tela("/inicio")
            else:
                erro_msg = data.get("error", {}).get("message", "Erro desconhecido")
                if "INVALID_LOGIN_CREDENTIALS" in erro_msg or "INVALID_PASSWORD" in erro_msg:
                    erro_msg = "E-mail ou senha incorretos."
                elif "EMAIL_EXISTS" in erro_msg:
                    erro_msg = "Este e-mail já está cadastrado."
                elif "WEAK_PASSWORD" in erro_msg:
                    erro_msg = "A senha deve ter pelo menos 6 caracteres."

                #page.open(ft.SnackBar(ft.Text(f"Erro: {erro_msg}"), bgcolor=ft.Colors.RED_400))
                snack = ft.SnackBar(ft.Text(f"Erro: {erro_msg}"), bgcolor=ft.Colors.RED_400)
                page.overlay.append(snack)
                snack.open = True
                page.update()

        except Exception as ex:
            erro_conexao = ft.SnackBar(ft.Text(f"Erro de conexão: {ex}"), bgcolor=ft.Colors.RED_400)
            page.overlay.append(erro_conexao)
            erro_conexao.open = True
            page.update()
    cabecalho = criar_cabecalho(COR_TEXTO_TITULO, COR_TEXTO_SECUNDARIO)

    btn_login = ft.ElevatedButton(
        "Sign In", bgcolor=COR_PRIMARIA, color=ft.Colors.WHITE,
        width=float("inf"),
        height=45, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        on_click=fazer_login,
    )

    secao_social = criar_login_social(COR_TEXTO_SECUNDARIO, COR_BORDA)
    rodape_termos = criar_rodape_termos(COR_TEXTO_SECUNDARIO, COR_PRIMARIA)

    funcao_alternar = obter_funcao_alternar(
        btn_aba_signin, btn_aba_signup, campo_nome, opcoes_extras, btn_login, COR_TEXTO_TITULO, COR_PRIMARIA
    )
    btn_aba_signin.on_click = funcao_alternar
    btn_aba_signup.on_click = funcao_alternar

    cabecalho_abas = ft.Row(controls=[btn_aba_signin, btn_aba_signup], alignment=ft.MainAxisAlignment.CENTER, spacing=10)

    card_login = criar_card_login(
        cabecalho_abas, campo_nome, campo_email, campo_senha, opcoes_extras, btn_login, secao_social, COR_CARD
    )

    return ft.View(
        route="/", 
        bgcolor=COR_FUNDO,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        padding=20, 
        controls=[ft.Container(content=ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=30, controls=[cabecalho, card_login, rodape_termos]))],
    )