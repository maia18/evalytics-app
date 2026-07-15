""" Importações """
import flet as ft
from components.layout.sidebar import Sidebar
from components.layout.topbar import TopBar
from components.core.theme import AppColors, get_app_theme # Design System

class ResponsiveLayout:
    def __init__(self, page: ft.Page, titulo_pagina: str, subtitulo: str = "", mudar_tela=None):
        self.page = page
        self.titulo_pagina = titulo_pagina
        self.subtitulo = subtitulo
        self.mudar_tela = mudar_tela
        
        self.dark_mode = getattr(self.page, "is_dark_mode", False)
        
        # Aplica o tema global na página
        self.page.theme = get_app_theme(self.dark_mode)
        self.page.theme_mode = ft.ThemeMode.DARK if self.dark_mode else ft.ThemeMode.LIGHT
        
        self.cores = AppColors.get(self.dark_mode)
        
        self.sidebar_mobile_aberta = False
        self.sidebar_colapsada = False
        self.conteudo_principal = ft.Column()
        
        self._criar_componentes()
    
    def _criar_componentes(self):
        self.overlay = ft.Container(
            visible=False, expand=True, bgcolor=AppColors.OVERLAY_MODAL,
            on_click=lambda e: self._fechar_sidebar(),
        )
        
        # Olha como a instância da Sidebar fica mais limpa!
        self.sidebar_desktop = Sidebar(
            dark_mode=self.dark_mode, mudar_tela=self.mudar_tela, collapsed=False
        )

        self.sidebar_mobile = ft.Container(
            left=-270, top=0, bottom=0, width=250,
            animate_position=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
            shadow=ft.BoxShadow(blur_radius=25, spread_radius=2, color="#33000000"),
            content=Sidebar(dark_mode=self.dark_mode, mudar_tela=self.mudar_tela, collapsed=False)
        )
        
        # A TopBar também perdeu 4 parâmetros desnecessários!
        self.topbar = TopBar(
            titulo_pagina=self.titulo_pagina,
            subtitulo=self.subtitulo,
            dark_mode=self.dark_mode,
            toggle_sidebar=self._toggle_sidebar,
            atualizar_tema=self._toggle_dark_mode
        )
    
    def _toggle_sidebar(self):
        """Abre ou fecha a sidebar mobile"""
        if self.page.width >= 900:
            return
        if self.sidebar_mobile_aberta:
            self._fechar_sidebar()
        else:
            self._abrir_sidebar()
    
    def _abrir_sidebar(self):
        """Abre a sidebar mobile"""
        self.sidebar_mobile_aberta = True
        self.sidebar_mobile.left = 0
        self.overlay.visible = True
        self.page.update()
    
    def _fechar_sidebar(self):
        """Fecha a sidebar mobile"""
        self.sidebar_mobile_aberta = False
        self.sidebar_mobile.left = -270
        self.overlay.visible = False
        self.page.update()
    
    def _toggle_dark_mode(self):
        """Atualiza as cores, salva o estado e recarrega a tela para aplicar o tema"""
        self.dark_mode = not self.dark_mode
        self.page.is_dark_mode = self.dark_mode
        
        self.page.theme_mode = ft.ThemeMode.DARK if self.dark_mode else ft.ThemeMode.LIGHT
        self.page.update()
        
        if self.mudar_tela and hasattr(self, 'rota_atual'):
            self.mudar_tela(self.rota_atual)
    
    def _ajustar_responsividade(self, e=None):
        """Ajusta a visibilidade e o tamanho dos componentes refatorados conforme o tamanho da tela"""
        
        if self.page.width < 700:
            self.sidebar_desktop.visible = False
            self.sidebar_desktop.width = 0
            self.topbar.menu_button.visible = True
        else:
            self.sidebar_desktop.visible = True
            self.topbar.menu_button.visible = False
            self._fechar_sidebar() 
            
            if self.page.width >= 1100:
                self.sidebar_desktop.width = 250
                # Removidos os parâmetros de cores antigas (COR_PRIMARIA, etc.)
                self.sidebar_desktop.content = Sidebar(
                    dark_mode=self.dark_mode,
                    mudar_tela=self.mudar_tela,
                    collapsed=False
                ).content
            else:
                self.sidebar_desktop.width = 72
                # Removidos os parâmetros de cores antigas
                self.sidebar_desktop.content = Sidebar(
                    dark_mode=self.dark_mode,
                    mudar_tela=self.mudar_tela,
                    collapsed=True
                ).content
        
        self.page.update()
    
    def add_content(self, content: ft.Control):
        """Adiciona conteúdo à área principal"""
        self.conteudo_principal = content
    
    def criar_view(self, route: str):
        """Cria e retorna a View com o layout responsivo"""
        
        self.rota_atual = route
        self.page.on_resize = self._ajustar_responsividade
        self._ajustar_responsividade()
        
        return ft.View(
            route=route,
            padding=0,
            bgcolor=self.cores["FUNDO"],
            controls=[
                ft.Stack(
                    expand=True,
                    controls=[
                        ft.Row(
                            expand=True,
                            spacing=0,
                            controls=[
                                self.sidebar_desktop,
                                ft.Column(
                                    expand=True,
                                    spacing=0,
                                    controls=[
                                        self.topbar,
                                        ft.Container(
                                            expand=True,
                                            padding=20,
                                            content=self.conteudo_principal
                                        )
                                    ], 
                                    scroll=ft.ScrollMode.AUTO
                                )
                            ]
                        ),
                        self.overlay,
                        self.sidebar_mobile
                    ]
                )
            ]
        )