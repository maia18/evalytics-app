import flet as ft 
from components.core.theme.theme import AppColors 
from components.layout.topbar.topbar_content import criar_topbar_content 
from components.core.constants.constants import * 

class TopBar(ft.Container): 
    """
    Componente principal da barra superior (TopBar).
    Herda de ft.Container para permitir estilização estrutural de fundo e bordas.
    """
    def __init__(self, titulo_pagina: str, subtitulo: str, dark_mode: bool, toggle_sidebar, atualizar_tema): 
        super().__init__() 

        self.titulo_pagina = titulo_pagina 
        self.subtitulo = subtitulo 
        self.dark_mode = dark_mode 
        self._toggle_sidebar = toggle_sidebar # Callback acionado para abrir/fechar o menu lateral mobile
        self._atualizar_tema = atualizar_tema # Callback acionado para inverter as cores do sistema

        # Puxa cores do Design System
        self.cores = AppColors.get(self.dark_mode) 

        # Botão de menu (Ícone Hamburguer)
        # Este botão tem a visibilidade controlada pela lógica de responsividade
        self.menu_button = ft.IconButton( 
            icon=ft.Icons.MENU, 
            on_click=lambda e: self._toggle_sidebar(), 
        ) 

        # Estilo visual
        self.bgcolor = self.cores[CARD] # Utiliza a cor de cartão do tema atual
        self.padding = 20 # Espaçamento interno padrão da barra
        # Adiciona uma borda delimitadora sutil apenas na parte inferior
        self.border = ft.Border(bottom=ft.BorderSide(1, self.cores[BORDA])) 

        # Conteúdo da TopBar
        # Delega a montagem dos elementos da linha para a função construtora do conteúdo
        self.content = criar_topbar_content( 
            titulo=self.titulo_pagina, 
            subtitulo=self.subtitulo, 
            dark_mode=self.dark_mode, 
            cores=self.cores, 
            menu_button=self.menu_button, 
            atualizar_tema=self._atualizar_tema 
        ) 