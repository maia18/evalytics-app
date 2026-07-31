import flet as ft
from typing import Callable
from components.core.theme.theme import AppColors
from components.core.constants.constants import CARD, BORDA
from components.layout.topbar.topbar_content import criar_topbar_content

class TopBar(ft.Container):
    """Componente principal da barra superior (TopBar).

    Herda de ft.Container para permitir estilização estrutural de fundo e bordas.
    """
    def __init__(
        self,
        titulo_pagina: str,
        subtitulo: str,
        dark_mode: bool,
        toggle_sidebar: Callable[[], None],
        atualizar_tema: Callable[[], None],
    ) -> None:
        super().__init__()

        self.titulo_pagina = titulo_pagina
        self.subtitulo = subtitulo
        self.dark_mode = dark_mode
        self._toggle_sidebar = toggle_sidebar
        self._atualizar_tema = atualizar_tema

        self.cores = AppColors.get(self.dark_mode) # Resgata a paleta de cores apropriada com base no estado de dark_mode

        # Cria o botão de menu (hamburguer) que, ao ser clicado, chamará o callback recebido por parâmetro
        self.menu_button = ft.IconButton(
            icon=ft.Icons.MENU,
            on_click=lambda e: self._toggle_sidebar(),
        )
        
        # Estilização estrutural do container
        self.bgcolor = self.cores[CARD]
        self.padding = 20
        
        self.border = ft.Border(bottom=ft.BorderSide(1, self.cores[BORDA])) # Adiciona uma borda apenas na parte inferior (bottom) para criar uma linha divisória limpa
        
        # Delega a criação dos elementos internos (Textos, Avatar, Icones) para a função importada
        self.content = criar_topbar_content(
            titulo=self.titulo_pagina,
            subtitulo=self.subtitulo,
            dark_mode=self.dark_mode,
            cores=self.cores,
            menu_button=self.menu_button,
            atualizar_tema=self._atualizar_tema,
        )