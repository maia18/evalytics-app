import flet as ft
from components.layout.sidebar.sidebar_toggle import toggle_sidebar
from components.core.theme.darkmode_toggle import toggle_dark_mode
from components.layout.responsive.responsiveness import ajustar_responsividade

class LayoutController:
    """Controlador responsável por gerenciar os estados e eventos do layout responsivo."""
    
    def __init__(self, page: ft.Page, mudar_tela):
        self.page = page
        self.mudar_tela = mudar_tela
        self.rota_atual = None
        
        self.sidebar_mobile_aberta = False
        self.dark_mode = getattr(page, "is_dark_mode", False)

        # Referências aos componentes visuais
        self.sidebar_mobile = None
        self.sidebar_desktop = None
        self.topbar = None
        self.overlay = None

    def registrar_componentes(self, sidebar_mobile, sidebar_desktop, topbar, overlay):
        """Salva a referência dos componentes instanciados para manipulá-los depois."""
        self.sidebar_mobile = sidebar_mobile
        self.sidebar_desktop = sidebar_desktop
        self.topbar = topbar
        self.overlay = overlay

    def abrir_sidebar(self):
        self.sidebar_mobile_aberta = True
        if self.sidebar_mobile: self.sidebar_mobile.left = 0
        if self.overlay: self.overlay.visible = True
        self.page.update()

    def fechar_sidebar(self):
        self.sidebar_mobile_aberta = False
        if self.sidebar_mobile: self.sidebar_mobile.left = -270
        if self.overlay: self.overlay.visible = False
        self.page.update()

    def toggle_sidebar(self):
        self.sidebar_mobile_aberta = toggle_sidebar(
            self.page,
            self.sidebar_mobile_aberta,
            self.abrir_sidebar,
            self.fechar_sidebar,
        )

    def toggle_dark_mode(self):
        self.dark_mode = toggle_dark_mode(
            self.page,
            self.dark_mode,
            self.mudar_tela,
            self.rota_atual,
        )

    def ajustar_responsividade(self, e=None):
        ajustar_responsividade(
            self.page,
            self.sidebar_desktop,
            self.topbar,
            self.fechar_sidebar,
            self.dark_mode,
            self.mudar_tela,
        )

        # Mantém o painel de notificações acima do conteúdo na posição correta.
        if self.topbar and hasattr(self.topbar, "painel_notificacoes"):
            painel = self.topbar.painel_notificacoes
            painel.right = 66
            painel.top = 66