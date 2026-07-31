from typing import Callable, Optional

import flet as ft

from components.layout.sidebar.sidebar import Sidebar

# Geometria e animação da sidebar mobile (gaveta deslizante).
# Centralizado aqui para evitar magic numbers duplicados em outros arquivos
# (ex.: responsive.py usa estas mesmas posições ao abrir/fechar a sidebar).
LARGURA_SIDEBAR_MOBILE = 250
POSICAO_SIDEBAR_MOBILE_FECHADA = -270  # Largura + margem de segurança fora da tela
POSICAO_SIDEBAR_MOBILE_ABERTA = 0
DURACAO_ANIMACAO_SIDEBAR_MS = 300
SOMBRA_SIDEBAR_MOBILE = "#33000000"


def criar_sidebar_desktop(dark_mode: bool, mudar_tela: Optional[Callable[[str], None]], collapsed: bool = False) -> Sidebar:
    """Instancia a Sidebar diretamente no modo Desktop (fica fixa na tela)."""
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