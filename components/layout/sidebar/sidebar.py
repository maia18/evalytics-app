import flet as ft
from components.core.theme.theme import AppColors
from components.layout.sidebar.sidebar_content import criar_sidebar_content
from components.layout.sidebar.sidebar_collapsed import criar_sidebar_colapsada

class Sidebar(ft.Container):
    
    """
    Sidebar reutilizável integrada ao Design System.
    """

    def __init__(self, dark_mode: bool, mudar_tela, collapsed=False):
        super().__init__()

        self.dark_mode = dark_mode
        self.mudar_tela = mudar_tela
        self.collapsed = collapsed

        # Cores dinâmicas
        self.cores = AppColors.get(self.dark_mode)

        # Estilo visual
        self.bgcolor = self.cores["CARD"]
        self.padding = 20
        self.border = ft.Border(right=ft.BorderSide(1, self.cores["BORDA"]))
        self.width = 72 if collapsed else 250

        # Conteúdo
        self.content = (
            criar_sidebar_colapsada(self.dark_mode, self.mudar_tela, self.cores)
            if collapsed else
            criar_sidebar_content(self.dark_mode, self.mudar_tela, self.cores)
        )
