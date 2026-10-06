import flet as ft

from components.layout.responsive.overlay import criar_overlay
from components.layout.sidebar.sidebar_factory import (
    criar_sidebar_desktop,
    criar_sidebar_mobile,
)
from components.layout.topbar.topbar_factory import criar_topbar
from components.layout.sidebar.sidebar_toggle import toggle_sidebar
from components.core.theme.theme_config import configurar_tema
from components.core.theme.darkmode_toggle import toggle_dark_mode
from components.layout.responsive.responsiveness import ajustar_responsividade
from components.layout.responsive.view_builder import montar_view


# Gerenciador central do layout responsivo, unindo sidebar, topbar e conteúdo
class ResponsiveLayout:

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

        self.dark_mode = getattr(
            self.page,
            "is_dark_mode",
            False,
        )

        self.sidebar_mobile_aberta = False
        self.conteudo_principal = ft.Column()

        self.cores = configurar_tema(
            self.page,
            self.dark_mode,
        )

        self._criar_componentes()

    # ==========================================================
    # CRIAÇÃO DOS COMPONENTES
    # ==========================================================

    def _criar_componentes(self):
        self.overlay = criar_overlay(
            self._fechar_sidebar
        )

        self.sidebar_desktop = criar_sidebar_desktop(
            page=self.page,
            dark_mode=self.dark_mode,
            mudar_tela=self.mudar_tela,
            collapsed=False,
        )

        self.sidebar_mobile = criar_sidebar_mobile(
            page=self.page,
            dark_mode=self.dark_mode,
            mudar_tela=self.mudar_tela,
        )

        self.topbar = criar_topbar(
            self.titulo_pagina,
            self.subtitulo,
            self.dark_mode,
            self._toggle_sidebar,
            self._toggle_dark_mode,
        )

        # ======================================================
        # PAINEL DE NOTIFICAÇÕES
        # ======================================================
        #
        # O painel não fica dentro da TopBar.
        # Ele é colocado no overlay da página para ficar acima
        # de todo o conteúdo da aplicação.
        #
        if hasattr(self.topbar, "painel_notificacoes"):
            self.page.overlay.append(
                self.topbar.painel_notificacoes
            )

    # ==========================================================
    # SIDEBAR
    # ==========================================================

    def _toggle_sidebar(self):
        self.sidebar_mobile_aberta = toggle_sidebar(
            self.page,
            self.sidebar_mobile_aberta,
            self._abrir_sidebar,
            self._fechar_sidebar,
        )

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

    # ==========================================================
    # TEMA
    # ==========================================================

    def _toggle_dark_mode(self):
        self.dark_mode = toggle_dark_mode(
            self.page,
            self.dark_mode,
            self.mudar_tela,
            getattr(self, "rota_atual", None),
        )

    # ==========================================================
    # RESPONSIVIDADE
    # ==========================================================

    def _ajustar_responsividade(self, e=None):
        ajustar_responsividade(
            self.page,
            self.sidebar_desktop,
            self.topbar,
            self._fechar_sidebar,
            self.dark_mode,
            self.mudar_tela,
        )

        # Mantém o painel de notificações acima do conteúdo.
        if hasattr(self.topbar, "painel_notificacoes"):
            painel = self.topbar.painel_notificacoes

            painel.right = 66
            painel.top = 66

    # ==========================================================
    # CONTEÚDO
    # ==========================================================

    def add_content(
        self,
        content: ft.Control,
    ):
        self.conteudo_principal = content

    # ==========================================================
    # VIEW
    # ==========================================================

    def criar_view(
        self,
        route: str,
    ):
        self.rota_atual = route

        self.page.on_resize = (
            self._ajustar_responsividade
        )

        self._ajustar_responsividade()

        return montar_view(
            route,
            self.cores,
            self.sidebar_desktop,
            self.topbar,
            self.conteudo_principal,
            self.overlay,
            self.sidebar_mobile,
            self._ajustar_responsividade,
            self.page,
        )