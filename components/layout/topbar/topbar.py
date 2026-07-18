import flet as ft
from components.core.theme.theme import AppColors
from components.layout.topbar.topbar_content import criar_topbar_content
from components.core.constants.constants import *

class TopBar(ft.Container):
    def __init__(self, titulo_pagina: str, subtitulo: str, dark_mode: bool, toggle_sidebar, atualizar_tema):
        super().__init__()

        self.titulo_pagina = titulo_pagina
        self.subtitulo = subtitulo
        self.dark_mode = dark_mode
        self._toggle_sidebar = toggle_sidebar
        self._atualizar_tema = atualizar_tema

        # Puxa cores do Design System
        self.cores = AppColors.get(self.dark_mode)

        # Botão de menu
        self.menu_button = ft.IconButton(
            icon=ft.Icons.MENU,
            on_click=lambda e: self._toggle_sidebar(),
        )

        # Estilo visual
        self.bgcolor = self.cores[CARD]
        self.padding = 20
        self.border = ft.Border(bottom=ft.BorderSide(1, self.cores[BORDA]))

        # Conteúdo da TopBar
        self.content = criar_topbar_content(
            titulo=self.titulo_pagina,
            subtitulo=self.subtitulo,
            dark_mode=self.dark_mode,
            cores=self.cores,
            menu_button=self.menu_button,
            atualizar_tema=self._atualizar_tema
        )