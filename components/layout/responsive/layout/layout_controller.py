import flet as ft
from components.layout.sidebar.sidebar_toggle import toggle_sidebar
from components.core.theme.darkmode_toggle import toggle_dark_mode
from components.layout.responsive.responsiveness import ajustar_responsividade

class LayoutController:
    """
    Controlador de Eventos e Estado (Controller do padrão MVC).
        Guarda as referências dos componentes visuais para manipulá-los dinamicamente sem a necessidade de recriar a interface inteira.
    """
    
    def __init__(self, page: ft.Page, mudar_tela):
        self.page = page
        self.mudar_tela = mudar_tela
        self.rota_atual = None
        self.sidebar_mobile_aberta = False
        self.dark_mode = getattr(page, "is_dark_mode", False) # Resgata o tema atual global da página. Se não existir, assume Claro (False)

        # Referências aos componentes da UI (Preenchidas via `registrar_componentes`)
        self.sidebar_mobile = None
        self.sidebar_desktop = None
        self.topbar = None
        self.overlay = None

    def registrar_componentes(self, sidebar_mobile, sidebar_desktop, topbar, overlay):
        """Salva a referência física dos componentes na memória do Controller."""
        
        self.sidebar_mobile = sidebar_mobile
        self.sidebar_desktop = sidebar_desktop
        self.topbar = topbar
        self.overlay = overlay

    def abrir_sidebar(self):
        """Desliza o menu lateral mobile para dentro da tela e aciona o overlay escuro."""
        
        self.sidebar_mobile_aberta = True
        if self.sidebar_mobile: 
            self.sidebar_mobile.left = 0  # 0 = Colado na borda esquerda da tela
            
        if self.overlay: 
            self.overlay.visible = True
            
        self.page.update() # FUNDAMENTAL: Avisa ao Flet para repintar a tela e mostrar a animação

    def fechar_sidebar(self):
        """Esconde a barra mobile jogando sua posição para fora da tela."""
        
        self.sidebar_mobile_aberta = False
        if self.sidebar_mobile: 
            self.sidebar_mobile.left = -270  # Joga o menu para fora da área visível (negativo)
            
        if self.overlay: 
            self.overlay.visible = False
            
        self.page.update()

    def toggle_sidebar(self):
        """Inverte o estado do menu (Se aberto, fecha. Se fechado, abre)."""
        
        self.sidebar_mobile_aberta = toggle_sidebar(
            self.page,
            self.sidebar_mobile_aberta,
            self.abrir_sidebar,
            self.fechar_sidebar,
        )

    def toggle_dark_mode(self):
        """Muda o tema e reconstrói a tela para aplicar as novas cores."""
        
        self.dark_mode = toggle_dark_mode(
            self.page,
            self.dark_mode,
            self.mudar_tela,
            self.rota_atual,
        )

    def ajustar_responsividade(self, e=None):
        """
        Callback executado sempre que o tamanho do navegador muda.
            Avalia a largura da tela e decide se oculta/mostra os componentes Desktop ou Mobile.
        """
        
        ajustar_responsividade(
            self.page,
            self.sidebar_desktop,
            self.topbar,
            self.fechar_sidebar,
            self.dark_mode,
            self.mudar_tela,
        )

        '''
        GARANTIA DE POSICIONAMENTO:
            Elementos do tipo 'Overlay' (como o painel flutuante de notificações) ignoram layouts padrão.
                Precisamos ancorá-los manualmente usando coordenadas absolutas (top, right).
        '''
        if self.topbar and hasattr(self.topbar, "painel_notificacoes"):
            painel = self.topbar.painel_notificacoes
            painel.right = 66
            painel.top = 66