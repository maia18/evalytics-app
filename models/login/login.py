from typing import Callable
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
    """
    Constrói a tela de Login e Registro (ponto de entrada da aplicação).
    
    NOTA ARQUITETURAL: esta tela usa as constantes de cor do modo claro diretamente,
    então não se adapta ao modo escuro automaticamente. Validar se isso é intencional para a identidade da marca.
    """
    
    # Autenticação simulada: por ora, apenas redireciona para a tela inicial
    def fazer_login(e: ft.ControlEvent) -> None:
        mudar_tela("/inicio")

    cabecalho = criar_cabecalho(COR_TEXTO_TITULO, COR_TEXTO_SECUNDARIO)

    # Prepara os inputs visuais do formulário.
    campo_nome = criar_campo_nome(COR_TEXTO_TITULO, COR_TEXTO_SECUNDARIO, COR_BORDA)
    campo_email = criar_campo_email(COR_TEXTO_TITULO, COR_TEXTO_SECUNDARIO, COR_BORDA)
    campo_senha = criar_campo_senha(COR_TEXTO_TITULO, COR_TEXTO_SECUNDARIO, COR_BORDA)

    opcoes_extras = criar_opcoes_extras(COR_TEXTO_SECUNDARIO, COR_PRIMARIA)

    btn_login = ft.ElevatedButton(
        "Sign In", bgcolor=COR_PRIMARIA, color=ft.Colors.WHITE,
        width=float("inf"),  # Preenche toda a largura do contêiner pai (padrão Flet)
        height=45, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        on_click=fazer_login,
    )

    secao_social = criar_login_social(COR_TEXTO_SECUNDARIO, COR_BORDA)
    rodape_termos = criar_rodape_termos(COR_TEXTO_SECUNDARIO, COR_PRIMARIA)

    # === Lógica de Abas para Alternar entre Login e Cadastro ===
    btn_aba_signin = ft.TextButton(
        "Entrar", data="signin", expand=True,
        style=criar_estilo_aba(ativo=True, cor_primaria=COR_PRIMARIA, cor_texto_inativo=COR_TEXTO_TITULO),
    )
    btn_aba_signup = ft.TextButton(
        "Cadastrar-se", data="signup", expand=True,
        style=criar_estilo_aba(ativo=False, cor_primaria=COR_PRIMARIA, cor_texto_inativo=COR_TEXTO_SECUNDARIO),
    )

    # Obtém o controlador que fará a lógica de ocultar o campo de 'Nome' ao entrar e mostrar ao cadastrar.
    funcao_alternar = obter_funcao_alternar(
        btn_aba_signin, btn_aba_signup, campo_nome, opcoes_extras, btn_login, COR_TEXTO_TITULO, COR_PRIMARIA
    )
    btn_aba_signin.on_click = funcao_alternar
    btn_aba_signup.on_click = funcao_alternar

    cabecalho_abas = ft.Row(controls=[btn_aba_signin, btn_aba_signup], alignment=ft.MainAxisAlignment.CENTER, spacing=10)

    # Passa todos os elementos renderizados acima para dentro do Card do Form.
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