from typing import Callable

import flet as ft

from components.core.theme.theme import AppColors
from components.layout.sidebar.sidebar_content import criar_sidebar_content
from components.layout.sidebar.sidebar_collapsed import criar_sidebar_colapsada
from components.core.constants.constants import CARD, BORDA

LARGURA_SIDEBAR_EXPANDIDA = 250
LARGURA_SIDEBAR_COLAPSADA = 72


class Sidebar(ft.Container):
    """Componente customizado que atua como o esqueleto principal do menu lateral.

    Se adapta automaticamente às larguras expandida ou colapsada.
    """

    def __init__(self, dark_mode: bool, mudar_tela: Callable[[str], None], collapsed: bool = False) -> None:
        super().__init__()

        self.dark_mode = dark_mode
        self.mudar_tela = mudar_tela
        self.collapsed = collapsed  # Flag que indica se o menu está recolhido (só ícones)

        self.cores = AppColors.get(self.dark_mode)

        self.bgcolor = self.cores[CARD]
        self.padding = 20
        self.border = ft.Border(right=ft.BorderSide(1, self.cores[BORDA]))
        self.width = LARGURA_SIDEBAR_COLAPSADA if collapsed else LARGURA_SIDEBAR_EXPANDIDA

        self.content = (
            criar_sidebar_colapsada(self.dark_mode, self.mudar_tela, self.cores)
            if collapsed else
            criar_sidebar_content(self.dark_mode, self.mudar_tela, self.cores)
        )