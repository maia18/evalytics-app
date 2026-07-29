import flet as ft
from typing import Callable, Optional

from components.layout.responsive.overlay import criar_overlay
from components.layout.sidebar.sidebar_factory import criar_sidebar_desktop, criar_sidebar_mobile
from components.layout.topbar.topbar_factory import criar_topbar
from components.layout.sidebar.sidebar_toggle import toggle_sidebar
from components.core.theme.theme_config import configurar_tema
from components.core.theme.darkmode_toggle import toggle_dark_mode
from components.layout.responsive.responsiveness import ajustar_responsividade
from components.layout.responsive.view_builder import montar_view

class ResponsiveLayout:
    """Gerenciador central do layout responsivo, unindo sidebar, topbar e conteúdo."""

    def __init__(
        self,
        page: ft.Page,
        titulo_pagina: str,
        subtitulo: str = "",
        mudar_tela: Optional[Callable[[str], None]] = None,
    ) -> None:
        self.page = page
        self.titulo_pagina = titulo_pagina
        self.subtitulo = subtitulo
        self.mudar_tela = mudar_tela

        self.dark_mode: bool = getattr(self.page, "is_dark_mode", False)
        self.sidebar_mobile_aberta: bool = False
        self.rota_atual: Optional[str] = None  # Definida ao chamar criar_view()
        self.conteudo_principal: ft.Control = ft.Column()

        self.cores = configurar_tema(self.page, self.dark_mode)
        self._criar_componentes()

    def _criar_componentes(self) -> None:
        """Instancia e armazena os componentes individuais da interface."""
        self.overlay = criar_overlay(self._fechar_sidebar)
        self.sidebar_desktop = criar_sidebar_desktop(self.dark_mode, self.mudar_tela)
        self.sidebar_mobile = criar_sidebar_mobile(self.dark_mode, self.mudar_tela)
        self.topbar = criar_topbar(
            self.titulo_pagina, self.subtitulo, self.dark_mode, self._toggle_sidebar, self._toggle_dark_mode
        )

    def _toggle_sidebar(self) -> None:
        """Inverte o estado de abertura da sidebar mobile."""
        self.sidebar_mobile_aberta = toggle_sidebar(
            self.page, self.sidebar_mobile_aberta, self._abrir_sidebar, self._fechar_sidebar
        )

    def _abrir_sidebar(self) -> None:
        """Exibe a sidebar móvel e ativa o overlay."""
        self.sidebar_mobile_aberta = True
        self.sidebar_mobile.left = 0  # Move o menu para dentro da tela
        self.overlay.visible = True   # Mostra o fundo escuro
        self.page.update()

    def _fechar_sidebar(self) -> None:
        """Oculta a sidebar móvel e desativa o overlay."""
        self.sidebar_mobile_aberta = False
        self.sidebar_mobile.left = -270  # Move o menu para fora da tela (escondido)
        self.overlay.visible = False
        self.page.update()

    def _toggle_dark_mode(self) -> None:
        """Alterna entre os temas Claro e Escuro, reconfigurando a página."""
        self.dark_mode = toggle_dark_mode(self.page, self.dark_mode, self.mudar_tela, self.rota_atual)

    def _ajustar_responsividade(self, e: ft.ControlEvent = None) -> None:
        """Aciona o ajuste de layout com base na largura atual da janela."""
        ajustar_responsividade(self.page, self.sidebar_desktop, self.topbar, self._fechar_sidebar, self.dark_mode, self.mudar_tela)

    def add_content(self, content: ft.Control) -> None:
        """Define o controle (tela de fato) exibido na área central."""
        self.conteudo_principal = content

    def criar_view(self, route: str) -> ft.View:
        """Retorna o ft.View montado com todos os elementos posicionados."""
        self.rota_atual = route
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