import flet as ft
from components.layout.sidebar.sidebar_factory import (
    criar_sidebar_desktop, 
    criar_sidebar_mobile,
)
from components.core.theme.theme_config import configurar_tema
from components.layout.responsive.overlay import criar_overlay
from components.layout.topbar.topbar_factory import criar_topbar
from components.layout.responsive.view_builder import montar_view
from .layout.layout_controller import LayoutController

class ResponsiveLayout:
    """Gerenciador central do layout responsivo, unindo sidebar, topbar e conteúdo."""

    def __init__(
        self,
        page: ft.Page,
        titulo_pagina: str,
        subtitulo: str = "",
        mudar_tela=None,
    ):
        self.page = page
        self.titulo_pagina = titulo_pagina
        self.subtitulo = subtitulo
        self.mudar_tela = mudar_tela
        self.conteudo_principal = ft.Column()

        # Instancia o controlador que cuidará de todas as lógicas e eventos
        self.controller = LayoutController(page, mudar_tela)
        
        self.cores = configurar_tema(self.page, self.controller.dark_mode)

        self._criar_componentes()

    def _criar_componentes(self):
        overlay = criar_overlay(self.controller.fechar_sidebar)

        sidebar_desktop = criar_sidebar_desktop(
            page=self.page,
            dark_mode=self.controller.dark_mode,
            mudar_tela=self.mudar_tela,
            collapsed=False,
        )

        sidebar_mobile = criar_sidebar_mobile(
            page=self.page,
            dark_mode=self.controller.dark_mode,
            mudar_tela=self.mudar_tela,
        )

        topbar = criar_topbar(
            page=self.page,
            titulo=self.titulo_pagina,
            subtitulo=self.subtitulo,
            dark_mode=self.controller.dark_mode,
            toggle_sidebar=self.controller.toggle_sidebar,
            atualizar_tema=self.controller.toggle_dark_mode,
        )

        # Injeta as interfaces geradas no controlador
        self.controller.registrar_componentes(sidebar_mobile, sidebar_desktop, topbar, overlay)

        # Gerenciamento do Painel de notificações
        if hasattr(topbar, "painel_notificacoes"):
            painel = topbar.painel_notificacoes
            if painel not in self.page.overlay:
                self.page.overlay.append(painel)

    def add_content(self, content: ft.Control):
        self.conteudo_principal = content

    def criar_view(self, route: str) -> ft.View:
        self.controller.rota_atual = route
        
        # Delega o evento de redimensionamento ao controlador
        self.page.on_resize = self.controller.ajustar_responsividade
        self.controller.ajustar_responsividade()

        return montar_view(
            route,
            self.cores,
            self.controller.sidebar_desktop,
            self.controller.topbar,
            self.conteudo_principal,
            self.controller.overlay,
            self.controller.sidebar_mobile,
            self.controller.ajustar_responsividade,
            self.page,
        )