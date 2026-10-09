import requests
import flet as ft
from typing import Callable
from components.core.auth.auth_state import auth_state
from models.login.core.logica_abas import obter_funcao_alternar
from models.login.core.cabecalho_login import criar_cabecalho
from models.login.core.tab_style import criar_estilo_aba
from models.login.core.rodape import criar_rodape_termos
from models.login.widgets.card_login import criar_card_login
from models.login.widgets.social_login import criar_login_social
from models.login.widgets.extras_login import criar_opcoes_extras
from models.login.widgets.campos_login import (
    criar_campo_nome, 
    criar_campo_email, 
    criar_campo_senha,
)
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
    Constrói a View (página inteira) de Login e Cadastro.
        Gerencia o estado da requisição HTTP para o Firebase e o redirecionamento.
    """
    
    # Chave pública da API do Firebase para autenticação REST
    FIREBASE_API_KEY = "AIzaSyAqGHhj3-BihICWHvD70smkjcbP2D8Sxnk"


    """
    # =========================================================================
    # 1. INSTANCIAÇÃO DOS COMPONENTES BASE
    # =========================================================================
    """
    
    campo_nome = criar_campo_nome(COR_TEXTO_TITULO, COR_TEXTO_SECUNDARIO, COR_BORDA)
    campo_email = criar_campo_email(COR_TEXTO_TITULO, COR_TEXTO_SECUNDARIO, COR_BORDA)
    campo_senha = criar_campo_senha(COR_TEXTO_TITULO, COR_TEXTO_SECUNDARIO, COR_BORDA)
    
    # Desempacota as opções extras (Checkbox de Lembrar-me e Link de Esqueceu a Senha)
    opcoes_extras, checkbox_lembrar = criar_opcoes_extras(
        COR_TEXTO_SECUNDARIO,
        COR_PRIMARIA,
    )

    """
    # =========================================================================
    # 2. SISTEMA DE ABAS (ENTRAR / CADASTRAR)
    # =========================================================================
    """
    
    btn_aba_signin = ft.TextButton(
        "Entrar", 
        data="signin", # O 'data' é usado para identificar qual botão foi clicado
        expand=True,   # Faz os dois botões dividirem o espaço 50/50
        style=criar_estilo_aba(ativo=True, cor_primaria=COR_PRIMARIA, cor_texto_inativo=COR_TEXTO_TITULO),
    )
    btn_aba_signup = ft.TextButton(
        "Cadastrar-se", 
        data="signup", 
        expand=True,
        style=criar_estilo_aba(ativo=False, cor_primaria=COR_PRIMARIA, cor_texto_inativo=COR_TEXTO_SECUNDARIO),
    )

    """
    # =========================================================================
    # 3. LÓGICA DE NEGÓCIO (HTTP POST PARA O FIREBASE)
    # =========================================================================
    """
    
    async def fazer_login(e: ft.ControlEvent) -> None:
        """Coleta os dados, decide qual endpoint chamar (Login ou Cadastro) e persiste a sessão do usuário."""
        
        # Como campo_email é uma ft.Column (Rótulo + TextField), acessamos o TextField no índice 1 e pegamos seu `.value`.
        email = campo_email.controls[1].value.strip()
        senha = campo_senha.controls[1].value.strip()
        
        # Validação básica de Front-end
        if not email or not senha:
            snack = ft.SnackBar(ft.Text("Preencha e-mail e senha!"), bgcolor=ft.Colors.RED_400)
            page.overlay.append(snack) # No Flet moderno, SnackBars devem ir para o Overlay
            snack.open = True
            page.update()
            return

        # Verifica pela cor do botão se o usuário está na aba de Cadastro (Sign Up)
        is_signup = btn_aba_signup.style.color == COR_PRIMARIA if hasattr(btn_aba_signup.style, 'color') else False
        
        # Define o endpoint dinamicamente
        if is_signup:
            url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_API_KEY}"
        else:
            url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"

        payload = {
            "email": email,
            "password": senha,
            "returnSecureToken": True # Exige que o Firebase devolva os tokens de acesso
        }

        try:
            # Faz a requisição síncrona (A thread pausa aqui aguardando a API)
            response = requests.post(url, json=payload)
            data = response.json()

            if response.status_code == 200:
                lembrar_me = checkbox_lembrar.value is True # SUCESSO!

                # Aciona o State Manager Global para salvar os tokens localmente
                await auth_state.iniciar_sessao(
                    dados=data,
                    page=page,
                    lembrar_me=lembrar_me,
                )

                sucesso = ft.SnackBar(ft.Text("Autenticação realizada com sucesso!"), bgcolor=ft.Colors.GREEN_400)
                page.overlay.append(sucesso)
                sucesso.open = True
                page.update()

                # Redireciona para o Dashboard
                mudar_tela("/inicio")
                
            else:
                # TRATAMENTO DE ERROS DO FIREBASE
                erro_msg = data.get("error", {}).get("message", "Erro desconhecido")
                
                # Mapeamento para PT-BR amigável
                if "INVALID_LOGIN_CREDENTIALS" in erro_msg or "INVALID_PASSWORD" in erro_msg:
                    erro_msg = "E-mail ou senha incorretos."
                elif "EMAIL_EXISTS" in erro_msg:
                    erro_msg = "Este e-mail já está cadastrado."
                elif "WEAK_PASSWORD" in erro_msg:
                    erro_msg = "A senha deve ter pelo menos 6 caracteres."

                snack = ft.SnackBar(ft.Text(f"Erro: {erro_msg}"), bgcolor=ft.Colors.RED_400)
                page.overlay.append(snack)
                snack.open = True
                page.update()

        except Exception as ex:
            
            # Captura erros de rede (Sem internet, timeout)
            erro_conexao = ft.SnackBar(ft.Text(f"Erro de conexão: {ex}"), bgcolor=ft.Colors.RED_400)
            page.overlay.append(erro_conexao)
            erro_conexao.open = True
            page.update()
            
    """
    # =========================================================================
    # 4. MONTAGEM FINAL DA INTERFACE
    # =========================================================================
    """
    
    cabecalho = criar_cabecalho(COR_TEXTO_TITULO, COR_TEXTO_SECUNDARIO)

    # O botão principal da ação (Sign In / Create Account)
    btn_login = ft.ElevatedButton(
        "Sign In", bgcolor=COR_PRIMARIA, color=ft.Colors.WHITE,
        width=float("inf"), # float("inf") faz o botão ocupar 100% da largura disponível
        height=45, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        on_click=fazer_login,
    )

    secao_social = criar_login_social(COR_TEXTO_SECUNDARIO, COR_BORDA)
    rodape_termos = criar_rodape_termos(COR_TEXTO_SECUNDARIO, COR_PRIMARIA)

    # Injeta os componentes na fábrica de closure para gerenciar a troca de visualização
    funcao_alternar = obter_funcao_alternar(
        btn_aba_signin, btn_aba_signup, campo_nome, opcoes_extras, btn_login, COR_TEXTO_TITULO, COR_PRIMARIA
    )
    
    # Ambas as abas chamam a mesma função; a lógica interna descobre quem chamou
    btn_aba_signin.on_click = funcao_alternar
    btn_aba_signup.on_click = funcao_alternar

    cabecalho_abas = ft.Row(controls=[btn_aba_signin, btn_aba_signup], alignment=ft.MainAxisAlignment.CENTER, spacing=10)

    # Agrupa todos os campos dentro da estrutura do Card branco
    card_login = criar_card_login(
        cabecalho_abas, campo_nome, campo_email, campo_senha, opcoes_extras, btn_login, secao_social, COR_CARD
    )

    # Retorna o container `View` (Página de navegação real do Flet)
    return ft.View(
        route="/login", 
        bgcolor=COR_FUNDO,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        padding=20, 
        
        # A Column centraliza verticalmente o Header, o Card de Login e os Termos
        controls=[ft.Container(content=ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=30, controls=[cabecalho, card_login, rodape_termos]))],
    )