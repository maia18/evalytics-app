from typing import Callable

import flet as ft

from components.core.theme.theme import AppColors
from components.layout.topbar.topbar_content import criar_topbar_content
from components.core.constants.constants import CARD, BORDA


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

        self.cores = AppColors.get(self.dark_mode)

        self.menu_button = ft.IconButton(
            icon=ft.Icons.MENU,
            on_click=lambda e: self._toggle_sidebar(),
        )

        self.bgcolor = self.cores[CARD]
        self.padding = 20
        self.border = ft.Border(bottom=ft.BorderSide(1, self.cores[BORDA]))

        self.content = criar_topbar_content(
            titulo=self.titulo_pagina,
            subtitulo=self.subtitulo,
            dark_mode=self.dark_mode,
            cores=self.cores,
            menu_button=self.menu_button,
            atualizar_tema=self._atualizar_tema,
        )