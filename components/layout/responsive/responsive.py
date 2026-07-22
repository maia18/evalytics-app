import flet as ft 
from components.layout.responsive.overlay import criar_overlay 
from components.layout.sidebar.sidebar_factory import criar_sidebar_desktop, criar_sidebar_mobile 
from components.layout.topbar.topbar_factory import criar_topbar 
from components.layout.sidebar.sidebar_toggle import toggle_sidebar 
from components.core.theme.theme_config import configurar_tema 
from components.core.theme.darkmode_toggle import toggle_dark_mode 
from components.layout.responsive.responsiveness import ajustar_responsividade 
from components.layout.responsive.view_builder import criar_view 

# Gerenciador central do layout responsivo, unindo sidebar, topbar e conteúdo
class ResponsiveLayout: 
    
    def __init__(self, page: ft.Page, titulo_pagina: str, subtitulo: str = "", mudar_tela=None): 
        self.page = page # Armazena a referência principal da página Flet
        self.titulo_pagina = titulo_pagina # Define o título visível na Topbar
        self.subtitulo = subtitulo # Define o subtítulo opcional
        self.mudar_tela = mudar_tela # Função de roteamento/navegação

        self.dark_mode = getattr(self.page, "is_dark_mode", False) # Recupera ou inicializa o estado do tema escuro
        self.sidebar_mobile_aberta = False # Controla o estado de visibilidade da sidebar mobile
        self.conteudo_principal = ft.Column() # Inicializa o container de conteúdo principal vazio

        self.cores = configurar_tema(self.page, self.dark_mode) # Aplica as cores baseadas no tema atual
        self._criar_componentes() 
        
    # Instancia e armazena os componentes individuais da interface
    def _criar_componentes(self): 
        self.overlay = criar_overlay(self._fechar_sidebar) # Cria a película escura de fundo
        self.sidebar_desktop = criar_sidebar_desktop(self.dark_mode, self.mudar_tela) 
        self.sidebar_mobile = criar_sidebar_mobile(self.dark_mode, self.mudar_tela) 
        self.topbar = criar_topbar(self.titulo_pagina, self.subtitulo, self.dark_mode, self._toggle_sidebar, self._toggle_dark_mode) 

    # Inverte o estado de abertura da sidebar mobile
    def _toggle_sidebar(self): 
        self.sidebar_mobile_aberta = toggle_sidebar(self.page, self.sidebar_mobile_aberta, self._abrir_sidebar, self._fechar_sidebar) 

    # Exibe a sidebar móvel e ativa o overlay
    def _abrir_sidebar(self): 
        self.sidebar_mobile_aberta = True 
        self.sidebar_mobile.left = 0 # Move o menu para dentro da tela
        self.overlay.visible = True # Mostra o fundo escuro
        self.page.update() 

    # Oculta a sidebar móvel e desativa o overlay
    def _fechar_sidebar(self): 
        self.sidebar_mobile_aberta = False 
        self.sidebar_mobile.left = -270 # Move o menu para fora da tela (escondido)
        self.overlay.visible = False # Remove o fundo escuro
        self.page.update() 

    # Alterna entre os temas Claro e Escuro, reconfigurando a página
    def _toggle_dark_mode(self): 
        self.dark_mode = toggle_dark_mode(self.page, self.dark_mode, self.mudar_tela, getattr(self, 'rota_atual', None), configurar_tema) 

    # Aciona a função externa que redimensiona e ajusta a interface baseada na tela
    def _ajustar_responsividade(self, e=None): 
        ajustar_responsividade(self.page, self.sidebar_desktop, self.topbar, self._fechar_sidebar, self.dark_mode, self.mudar_tela) 

    # Adiciona o controle (Página de fato) à área de visualização central
    def add_content(self, content: ft.Control): 
        self.conteudo_principal = content 

    # Retorna o controle 'ft.View' montado com todos os elementos posicionados
    def criar_view(self, route: str): 
        self.rota_atual = route # Salva a rota atual em memória
        return criar_view(route, self.cores, self.sidebar_desktop, self.topbar, self.conteudo_principal, self.overlay, self.sidebar_mobile, self._ajustar_responsividade, self.page) 