import flet as ft
from typing import Callable, Optional
from components.layout.sidebar.sidebar import Sidebar
from components.core.constants.constants import (
    LARGURA_SIDEBAR_MOBILE,
    POSICAO_SIDEBAR_MOBILE_FECHADA,
    DURACAO_ANIMACAO_SIDEBAR_MS,
    SOMBRA_SIDEBAR_MOBILE,
)

def criar_sidebar_desktop(
    dark_mode: bool, 
    mudar_tela: Optional[Callable[[str], None]], 
    collapsed: bool = False
) -> Sidebar:
    """
    Instancia a Sidebar diretamente para a interface Desktop.
        Neste formato, o menu lateral fica fixo na estrutura da página (geralmente em uma Row).
    """
    
    # Retorna a classe Sidebar com suas propriedades nativas.
    return Sidebar(
        dark_mode=dark_mode, 
        mudar_tela=mudar_tela, 
        collapsed=collapsed,
    )


def criar_sidebar_mobile(
    dark_mode: bool, 
    mudar_tela: Optional[Callable[[str], None]]
) -> ft.Container:
    """
    Cria a Sidebar formatada para telas reduzidas (Mobile e Tablets).
        Neste cenário, a Sidebar atua como um "Drawer" (gaveta) flutuante que desliza para dentro e fora da tela por cima do conteúdo principal.
    """
    
    return ft.Container(
        # POSICIONAMENTO ABSOLUTO:
        # Quando usado dentro de um ft.Stack, 'top=0' e 'bottom=0' forçam o contêiner a esticar e ocupar 100% da altura da tela.
        top=0, 
        bottom=0, 
        
        # 'left' define a posição horizontal. 
        # Iniciamos com um valor negativo (ex: -300) para que o menu comece escondido fora da tela.
        left=POSICAO_SIDEBAR_MOBILE_FECHADA, 
        width=LARGURA_SIDEBAR_MOBILE,
        
        # ANIMAÇÃO:
        # Quando a propriedade 'left' for alterada via código (ex: left=0 para abrir), o Flet criará uma transição suave de deslizamento (EASE_OUT).
        animate_position=ft.Animation(
            DURACAO_ANIMACAO_SIDEBAR_MS, 
            ft.AnimationCurve.EASE_OUT
        ),
        
        # SOMBRA:
        # Como o menu mobile flutua sobre o restante do aplicativo, a sombra ajuda a separar os elementos visualmente.
        shadow=ft.BoxShadow(
            blur_radius=25, 
            spread_radius=2, 
            color=SOMBRA_SIDEBAR_MOBILE
        ),
        
        # Conteúdo interno é a própria classe Sidebar.
        content=Sidebar(
            dark_mode=dark_mode, 
            mudar_tela=mudar_tela, 
            collapsed=False
        ),
    )