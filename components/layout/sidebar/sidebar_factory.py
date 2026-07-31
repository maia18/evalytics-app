import flet as ft
from typing import Callable, Optional
from components.layout.sidebar.sidebar import Sidebar
from components.core.constants.constants import (
    LARGURA_SIDEBAR_MOBILE,
    POSICAO_SIDEBAR_MOBILE_FECHADA,
    DURACAO_ANIMACAO_SIDEBAR_MS,
    SOMBRA_SIDEBAR_MOBILE,
)

# Instancia a Sidebar diretamente no modo Desktop (fica fixa na tela)
def criar_sidebar_desktop(dark_mode: bool, mudar_tela: Optional[Callable[[str], None]], collapsed: bool = False) -> Sidebar:
    return Sidebar(dark_mode=dark_mode, mudar_tela=mudar_tela, collapsed=collapsed)

def criar_sidebar_mobile(dark_mode: bool, mudar_tela: Optional[Callable[[str], None]]) -> ft.Container:
    """Cria a Sidebar de navegação voltada para telas reduzidas (Mobile e Tablets verticais).

    O comportamento muda para um menu deslizante em forma de gaveta (Drawer).
    """
    return ft.Container(
        left=POSICAO_SIDEBAR_MOBILE_FECHADA, top=0, bottom=0, width=LARGURA_SIDEBAR_MOBILE,
        animate_position=ft.Animation(DURACAO_ANIMACAO_SIDEBAR_MS, ft.AnimationCurve.EASE_OUT),
        shadow=ft.BoxShadow(blur_radius=25, spread_radius=2, color=SOMBRA_SIDEBAR_MOBILE),
        content=Sidebar(dark_mode=dark_mode, mudar_tela=mudar_tela, collapsed=False),
    )