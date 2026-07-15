import flet as ft
from components.layout.responsive.overlay import criar_overlay
from components.layout.sidebar.sidebar_factory import criar_sidebar_desktop, criar_sidebar_mobile
from components.layout.topbar.topbar_factory import criar_topbar
from components.layout.sidebar.sidebar_toggle import toggle_sidebar
from components.core.theme.theme_config import configurar_tema
from components.core.theme.darkmode_toggle import toggle_dark_mode
from components.layout.responsive.responsiveness import ajustar_responsividade
from components.layout.responsive.view_builder import criar_view

class ResponsiveLayout:
    def __init__(self, page: ft.Page, titulo_pagina: str, subtitulo: str = "", mudar_tela=None):
        self.page = page
        self.titulo_pagina = titulo_pagina
        self.subtitulo = subtitulo
        self.mudar_tela = mudar_tela

        self.dark_mode = getattr(self.page, "is_dark_mode", False)
        self.sidebar_mobile_aberta = False
        self.conteudo_principal = ft.Column()

        self.cores = configurar_tema(self.page, self.dark_mode)
        self._criar_componentes()

    def _criar_componentes(self):
        self.overlay = criar_overlay(self._fechar_sidebar)
        self.sidebar_desktop = criar_sidebar_desktop(self.dark_mode, self.mudar_tela)
        self.sidebar_mobile = criar_sidebar_mobile(self.dark_mode, self.mudar_tela)
        self.topbar = criar_topbar(self.titulo_pagina, self.subtitulo, self.dark_mode, self._toggle_sidebar, self._toggle_dark_mode)

    def _toggle_sidebar(self):
        self.sidebar_mobile_aberta = toggle_sidebar(self.page, self.sidebar_mobile_aberta, self._abrir_sidebar, self._fechar_sidebar)

    def _abrir_sidebar(self):
        self.sidebar_mobile_aberta = True
        self.sidebar_mobile.left = 0
        self.overlay.visible = True
        self.page.update()

    def _fechar_sidebar(self):
        self.sidebar_mobile_aberta = False
        self.sidebar_mobile.left = -270
        self.overlay.visible = False
        self.page.update()

    def _toggle_dark_mode(self):
        self.dark_mode = toggle_dark_mode(self.page, self.dark_mode, self.mudar_tela, getattr(self, 'rota_atual', None), configurar_tema)

    def _ajustar_responsividade(self, e=None):
        ajustar_responsividade(self.page, self.sidebar_desktop, self.topbar, self._fechar_sidebar, self.dark_mode, self.mudar_tela)

    def add_content(self, content: ft.Control):
        self.conteudo_principal = content

    def criar_view(self, route: str):
        self.rota_atual = route
        return criar_view(route, self.cores, self.sidebar_desktop, self.topbar, self.conteudo_principal, self.overlay, self.sidebar_mobile, self._ajustar_responsividade, self.page)