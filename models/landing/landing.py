import flet as ft
from typing import Callable

from components.core.constants.constants import COR_FUNDO

# Componentes da landing page
from components.landing.header import criar_header
from components.landing.hero import criar_hero
from components.landing.recursos import criar_secao_recursos
from components.landing.sobre import criar_secao_sobre
from components.landing.cta import criar_cta
from components.landing.rodape import criar_rodape

def ViewLanding(page: ft.Page, mudar_tela: Callable[[str], None]) -> ft.View:
    """Cria e retorna a View principal da Landing Page."""

    # =========================================================
    # NAVEGAÇÃO INTERNA
    # =========================================================

    async def ir_para_recursos(e):
        """Navega até a seção de recursos da Landing Page."""

        await view.scroll_to(
            scroll_key="recursos",
            duration=500,
            curve=ft.AnimationCurve.EASE_IN_OUT,
        )

    async def ir_para_sobre(e):
        """Navega até a seção 'Sobre'."""

        await view.scroll_to(
            scroll_key="sobre",
            duration=500,
            curve=ft.AnimationCurve.EASE_IN_OUT,
        )

    # =========================================================
    # COMPONENTES
    # =========================================================

    # Cabeçalho da página contendo logo, menu e navegação.
    header = criar_header(
        page=page,
        mudar_tela=mudar_tela,
        ir_para_recursos=ir_para_recursos,
        ir_para_sobre=ir_para_sobre,
    )
    
    # Seção principal ("Hero") apresentada ao carregar a página.
    hero = criar_hero(
        mudar_tela=mudar_tela,
        ir_para_recursos=ir_para_recursos,
    )

    recursos = criar_secao_recursos() # Seção responsável por apresentar funcionalidades, recursos ou benefícios do sistema.

    sobre = criar_secao_sobre() # Seção contendo informações institucionais, contexto ou apresentação da plataforma.

    # CTA (Call To Action) - Área destinada a incentivar o usuário a executar uma ação importante (cadastro, login, contratação etc.).
    cta = criar_cta(
        mudar_tela=mudar_tela,
    )

    rodape = criar_rodape() # Rodapé contendo informações complementares, links úteis ou informações legais.

    # =========================================================
    # VIEW
    # =========================================================

    view = ft.View(
        route="/", # Rota principal da aplicação
        bgcolor=COR_FUNDO, # Cor de fundo definida nas constantes globais
        padding=0, # Remove espaçamento padrão da View
        scroll=ft.ScrollMode.AUTO, # Permite rolagem automática quando o conteúdo ultrapassar a altura da tela
        
        # Ordem de renderização dos componentes
        controls=[
            header,
            hero,
            recursos,
            sobre,
            cta,
            rodape,
        ],
    )
    return view