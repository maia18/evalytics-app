import flet as ft
from typing import Callable

from components.core.theme.theme import AppColors

from components.core.constants.constants import (
    CARD,
    BORDA,
    LARGURA_SIDEBAR_EXPANDIDA,
    LARGURA_SIDEBAR_COLAPSADA,
)

from components.layout.sidebar.sidebar_content import criar_sidebar_content
from components.layout.sidebar.sidebar_collapsed import criar_sidebar_colapsada


class Sidebar(ft.Container):
    """
    Componente customizado que atua como o esqueleto principal do menu lateral.
        Se adapta automaticamente às larguras expandida ou colapsada.
    """

    def __init__(
<<<<<<< HEAD
        self,
        page: ft.Page,
        dark_mode: bool,
        mudar_tela: Callable[[str], None],
        collapsed: bool = False,
    ) -> None:

        super().__init__()

        self.dark_mode = dark_mode
        self.mudar_tela = mudar_tela
        self.collapsed = collapsed

        self.cores = AppColors.get(self.dark_mode)

        self.bgcolor = self.cores[CARD]

        self.padding = 20

        self.border = ft.Border(
            right=ft.BorderSide(
                1,
                self.cores[BORDA],
            )
        )

        self.width = (
            LARGURA_SIDEBAR_COLAPSADA
            if collapsed
            else LARGURA_SIDEBAR_EXPANDIDA
        )

        if collapsed:
            self.content = criar_sidebar_colapsada(
                page=page,
                dark_mode=self.dark_mode,
                mudar_tela=self.mudar_tela,
                cores=self.cores,
            )
        else:
            self.content = criar_sidebar_content(
                page=page,
                dark_mode=self.dark_mode,
                mudar_tela=self.mudar_tela,
                cores=self.cores,
            )
=======
        self, 
        dark_mode: bool,
        mudar_tela: Callable[[str], None], 
        collapsed: bool = False
    ) -> None:
        super().__init__() # Inicializa a classe base (ft.Container) antes de aplicar nossas customizações
        
        # Salva as propriedades no estado da instância para uso futuro
        self.dark_mode = dark_mode
        self.mudar_tela = mudar_tela
        self.collapsed = collapsed  # Define o modo de exibição inicial
        
        self.cores = AppColors.get(self.dark_mode) # Resgata a paleta de cores correta baseada no tema atual (Claro ou Escuro)
        self.bgcolor = self.cores[CARD] # Fundo do menu lateral (geralmente branco no claro, cinza escuro/preto no escuro)
        
        self.padding = 20 # Respiro interno em todas as direções para o conteúdo não colar nas bordas da tela
        
        # Borda apenas na direita: cria uma linha separadora fina entre a sidebar e o conteúdo principal do app
        self.border = ft.Border(
            right=ft.BorderSide(1, self.cores[BORDA])
        )
        self.width = LARGURA_SIDEBAR_COLAPSADA if collapsed else LARGURA_SIDEBAR_EXPANDIDA # Verifica a flag `collapsed` para decidir qual constante de largura aplicar.
        
        # Renderiza os botões e a logo dependendo do estado solicitado.
        self.content = (
            criar_sidebar_colapsada(
                self.dark_mode, 
                self.mudar_tela, 
                self.cores,
            )
            if collapsed else
            criar_sidebar_content(
                self.dark_mode, 
                self.mudar_tela, 
                self.cores,
            )
        )
>>>>>>> ea794a06b2548ae4a0bed3f239fa3214c9fd367e
