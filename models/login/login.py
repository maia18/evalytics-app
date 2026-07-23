import flet as ft

# Importações dos módulos que constroem pedaços isolados da tela de login
from models.login.core.cabecalho_login import criar_cabecalho
from models.login.widgets.campos_login import criar_campo_nome, criar_campo_email, criar_campo_senha
from models.login.widgets.extras_login import criar_opcoes_extras
from models.login.widgets.card_login import criar_card_login
from models.login.widgets.social_login import criar_login_social
from models.login.core.rodape import criar_rodape_termos
from models.login.core.logica_abas import obter_funcao_alternar

# Importação das constantes visuais (cores, dimensões)
from components.core.constants.constants import *

def ViewLogin(page: ft.Page, mudar_tela):
    """
    Constrói a tela de Login e Registro (ponto de entrada da aplicação).
    Utiliza uma abordagem altamente modular, importando as seções da tela de arquivos separados.
    """

    def fazer_login(e):
        """
        Função simulada de autenticação. 
        Por enquanto, ignora as credenciais e apenas redireciona para a tela inicial ("/inicio").
        """
        mudar_tela("/inicio")

    # === Instanciação dos Componentes ===
    # Cria as partes da tela utilizando as cores padronizadas pelas constantes
    cabecalho = criar_cabecalho(COR_TEXTO_TITULO, COR_TEXTO_SECUNDARIO)
    
    # O campo nome é instanciado aqui, mas a lógica de abas definirá se ele ficará visível (Sign Up) ou oculto (Sign In)
    campo_nome = criar_campo_nome(COR_TEXTO_TITULO, COR_TEXTO_SECUNDARIO, COR_BORDA)
    campo_email = criar_campo_email(COR_TEXTO_TITULO, COR_TEXTO_SECUNDARIO, COR_BORDA)
    campo_senha = criar_campo_senha(COR_TEXTO_TITULO, COR_TEXTO_SECUNDARIO, COR_BORDA)
    
    # Opções extras de conveniência como "Lembrar de mim" e "Esqueci a senha"
    opcoes_extras = criar_opcoes_extras(COR_TEXTO_SECUNDARIO, COR_PRIMARIA)

    # Botão principal de ação do formulário
    btn_login = ft.ElevatedButton(
        "Sign In",
        bgcolor=COR_PRIMARIA,
        color="white",
        width=float("inf"), # width infinito instrui o botão a preencher toda a largura do seu contêiner pai
        height=45,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        on_click=fazer_login # Aciona a função simulada de redirecionamento ao clicar
    )
    
    # Seções auxiliares inferiores da tela
    secao_social = criar_login_social(COR_TEXTO_SECUNDARIO, COR_BORDA) # Botões de autenticação Google, Apple, etc.
    rodape_termos = criar_rodape_termos(COR_TEXTO_SECUNDARIO, COR_PRIMARIA) # Links de termos de uso e privacidade

    # === Lógica de Abas (Sign In / Sign Up) ===
    # Estilo base removendo o arredondamento para que os botões pareçam guias (abas) coladas umas nas outras
    estilo_aba = ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=0),
        color=COR_TEXTO_TITULO,
        bgcolor=COR_CARD 
    )
    
    # Aba de Sign In (Login)
    btn_aba_signin = ft.OutlinedButton("Sign In", data="signin", style=estilo_aba)
    btn_aba_signin.style.side = ft.border.BorderSide(1, COR_PRIMARIA) # Inicia em evidência com a cor primária
    
    # Aba de Sign Up (Cadastro)
    btn_aba_signup = ft.OutlinedButton("Sign Up", data="signup", style=estilo_aba)
    btn_aba_signup.style.side = ft.border.BorderSide(1, "transparent") # Inicia sem destaque de borda
    
    # Recupera a função de callback que reage à troca de abas.
    # Esta função manipulará o visual da tela (ex: exibindo o campo de nome ao ir para Sign Up).
    funcao_alternar = obter_funcao_alternar(
        btn_aba_signin, btn_aba_signup, campo_nome, opcoes_extras, 
        btn_login, COR_TEXTO_TITULO, COR_CARD, COR_PRIMARIA
    )
    
    # Acopla a função de alternância ao evento de clique de ambas as abas
    btn_aba_signin.on_click = funcao_alternar
    btn_aba_signup.on_click = funcao_alternar
    
    # Agrupa as abas em uma linha centralizada, com espaçamento zero (coladas)
    cabecalho_abas = ft.Row([btn_aba_signin, btn_aba_signup], alignment=ft.MainAxisAlignment.CENTER, spacing=0)
    
    # === Montagem do Card Principal ===
    # Encapsula todos os elementos de input e ações dentro do contêiner central da tela
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
        
    # === Retorno da View ===
    # Retorna a estrutura final da página, engessando-a na rota raiz ("/")
    return ft.View(
        route="/",
        bgcolor=COR_FUNDO,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER, # Centraliza todo o conteúdo horizontalmente
        vertical_alignment=ft.MainAxisAlignment.CENTER, # Centraliza todo o conteúdo verticalmente
        padding=20,
        controls=[
            ft.Container(
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=30, # Espaçamento amplo separando a marca, o painel de login e os termos
                    controls=[cabecalho, card_login, rodape_termos]
                )
            )
        ]
    )