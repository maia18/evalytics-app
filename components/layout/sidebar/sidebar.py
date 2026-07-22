import flet as ft 
from components.core.theme.theme import AppColors 
from components.layout.sidebar.sidebar_content import criar_sidebar_content 
from components.layout.sidebar.sidebar_collapsed import criar_sidebar_colapsada 
from components.core.constants.constants import * 

# Sidebar reutilizável integrada ao Design System
class Sidebar(ft.Container): 
    """
    Componente customizado que atua como o esqueleto principal do menu lateral.
    Ele se adapta automaticamente às larguras expandida ou colapsada.
    """
    
    def __init__(self, dark_mode: bool, mudar_tela, collapsed=False): 
        super().__init__() 

        self.dark_mode = dark_mode 
        self.mudar_tela = mudar_tela 
        self.collapsed = collapsed # Flag que indica se o menu está recolhido (só ícones)

        # Cores dinâmicas
        self.cores = AppColors.get(self.dark_mode) # Aplica as cores corretas com base no tema

        # Estilo visual
        self.bgcolor = self.cores[CARD] # Fundo da sidebar usa a cor definida para elementos tipo Card
        self.padding = 20 # Espaçamento interno padrão
        self.border = ft.Border(right=ft.BorderSide(1, self.cores[BORDA])) # Cria uma linha divisória sutil apenas no lado direito
        self.width = 72 if collapsed else 250 # Lógica de tamanho: 72px (apenas ícones) ou 250px (completo)

        # Conteúdo
        # Utiliza um operador condicional (ternário) para injetar o tipo correto de menu
        self.content = ( 
            criar_sidebar_colapsada(self.dark_mode, self.mudar_tela, self.cores) 
            if collapsed else 
            criar_sidebar_content(self.dark_mode, self.mudar_tela, self.cores) 
        ) 