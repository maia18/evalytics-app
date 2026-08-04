from typing import Callable

import flet as ft

from models.login.core.cabecalho_login import criar_cabecalho
from models.login.widgets.campos_login import criar_campo_nome, criar_campo_email, criar_campo_senha
from models.login.widgets.extras_login import criar_opcoes_extras
from models.login.widgets.card_login import criar_card_login
from models.login.widgets.social_login import criar_login_social
from models.login.core.rodape import criar_rodape_termos
from models.login.core.logica_abas import obter_funcao_alternar
from models.login.core.tab_style import criar_estilo_aba

from components.core.constants.constants import (
    COR_TEXTO_TITULO, COR_TEXTO_SECUNDARIO, COR_BORDA, COR_PRIMARIA, COR_CARD, COR_FUNDO,
)


def ViewLogin(page: ft.Page, mudar_tela: Callable[[str], None]) -> ft.View:
    """Constrói a tela de Login e Registro (ponto de entrada da aplicação).

    NOTA: esta tela usa as constantes de cor do modo claro diretamente (não
    `AppColors`/`layout.cores`), então não se adapta ao modo escuro salvo em
    sessões anteriores. Comportamento mantido como estava; validar se é
    intencional numa próxima decisão de produto.
    """

    def fazer_login(e: ft.ControlEvent) -> None:
        """Autenticação simulada: por ora, apenas redireciona para a tela inicial."""
        mudar_tela("/inicio")

    cabecalho = criar_cabecalho(COR_TEXTO_TITULO, COR_TEXTO_SECUNDARIO)

    campo_nome = criar_campo_nome(COR_TEXTO_TITULO, COR_TEXTO_SECUNDARIO, COR_BORDA)
    campo_email = criar_campo_email(COR_TEXTO_TITULO, COR_TEXTO_SECUNDARIO, COR_BORDA)
    campo_senha = criar_campo_senha(COR_TEXTO_TITULO, COR_TEXTO_SECUNDARIO, COR_BORDA)

    opcoes_extras = criar_opcoes_extras(COR_TEXTO_SECUNDARIO, COR_PRIMARIA)

    btn_login = ft.ElevatedButton(
        "Sign In",
        bgcolor=COR_PRIMARIA,
        color=ft.Colors.WHITE,
        width=float("inf"),  # Preenche toda a largura do contêiner pai (padrão documentado do Flet)
        height=45,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        on_click=fazer_login,
    )

    secao_social = criar_login_social(COR_TEXTO_SECUNDARIO, COR_BORDA)
    rodape_termos = criar_rodape_termos(COR_TEXTO_SECUNDARIO, COR_PRIMARIA)

    # === Abas Sign In / Sign Up ===
    btn_aba_signin = ft.TextButton(
        "Entrar", data="signin", expand=True,
        style=criar_estilo_aba(ativo=True, cor_primaria=COR_PRIMARIA, cor_texto_inativo=COR_TEXTO_TITULO),
    )
    btn_aba_signup = ft.TextButton(
        "Cadastrar-se", data="signup", expand=True,
        style=criar_estilo_aba(ativo=False, cor_primaria=COR_PRIMARIA, cor_texto_inativo=COR_TEXTO_SECUNDARIO),
    )

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
        controls=[
            ft.Container(
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=30,
                    controls=[cabecalho, card_login, rodape_termos],
                )
            )
        ],
    )