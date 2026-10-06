import asyncio
import flet as ft
from typing import Callable

from components.core.theme.theme import AppColors
from components.core.constants.constants import (
    CARD,
    BORDA,
)
from components.layout.topbar.topbar_content import (
    criar_topbar_content,
)
from components.layout.topbar.core.notifications import (
    contar_nao_lidas,
    listar_notificacoes,
)

class TopBar(ft.Container):
    """Componente principal da barra superior (TopBar)."""

    def __init__(
        self,
        page: ft.Page,
        titulo_pagina: str,
        subtitulo: str,
        dark_mode: bool,
        toggle_sidebar: Callable[[], None],
        atualizar_tema: Callable[[], None],
    ) -> None:

        super().__init__()
        
        self._page = page

        self.titulo_pagina = titulo_pagina
        self.subtitulo = subtitulo
        self.dark_mode = dark_mode

        self._toggle_sidebar = toggle_sidebar
        self._atualizar_tema = atualizar_tema

        # ======================================================
        # ESTADO DAS NOTIFICAÇÕES
        # ======================================================

        self.notificacoes_pendentes = 0

        # ======================================================
        # CORES
        # ======================================================

        self.cores = AppColors.get(
            self.dark_mode
        )

        # ======================================================
        # BOTÃO MENU
        # ======================================================

        self.menu_button = ft.IconButton(
            icon=ft.Icons.MENU,
            on_click=lambda e: self._toggle_sidebar(),
        )

        # ======================================================
        # ESTILIZAÇÃO DA TOPBAR
        # ======================================================

        self.bgcolor = self.cores[CARD]
        self.padding = 20

        self.border = ft.Border(
            bottom=ft.BorderSide(
                1,
                self.cores[BORDA],
            )
        )

        # ======================================================
        # CONTEÚDO
        # ======================================================

        self.content = criar_topbar_content(
            page=page,
            titulo=titulo_pagina,
            subtitulo=subtitulo,
            dark_mode=dark_mode,
            cores=self.cores,
            menu_button=self.menu_button,
            atualizar_tema=atualizar_tema,
            notificacoes_pendentes=self.notificacoes_pendentes,
        )

        # ======================================================
        # REFERÊNCIAS DO SISTEMA DE NOTIFICAÇÕES
        # ======================================================

        self.badge_notificacoes = getattr(
            self.content,
            "badge_notificacoes",
            None,
        )

        self.painel_notificacoes = getattr(
            self.content,
            "painel_notificacoes",
            None,
        )

        self.atualizar_lista_notificacoes = getattr(
            self.content,
            "atualizar_lista_notificacoes",
            None,
        )
        
        self._task_notificacoes = None

        if not getattr(
            self._page,
            "_monitor_notificacoes_iniciado",
            False,
        ):
            self._page._monitor_notificacoes_iniciado = True
            self._page._topbar_notificacoes = self

            self._task_notificacoes = self._page.run_task(
                self._monitorar_notificacoes
            )
        else:
            self._page._topbar_notificacoes = self

    # ==========================================================
    # ATUALIZAR NOTIFICAÇÕES
    # ==========================================================

    def atualizar_notificacoes(
        self,
        quantidade: int,
    ) -> None:
        """Atualiza a quantidade de notificações não lidas."""

        self.notificacoes_pendentes = max(
            0,
            quantidade,
        )

        if self.badge_notificacoes is None:
            return

        self.badge_notificacoes.visible = (
            self.notificacoes_pendentes > 0
        )

        self.badge_notificacoes.content = ft.Text(
            str(self.notificacoes_pendentes),
            size=9,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE,
        )
        
    async def _monitorar_notificacoes(self):

        while True:

            try:

                topbar_atual = getattr(
                    self._page,
                    "_topbar_notificacoes",
                    None,
                )

                if topbar_atual is not None:

                    # ==========================================
                    # ATUALIZA O CONTADOR
                    # ==========================================

                    quantidade = await asyncio.to_thread(
                        contar_nao_lidas
                    )

                    topbar_atual.atualizar_notificacoes(
                        quantidade
                    )

                    # ==========================================
                    # ATUALIZA A LISTA DO PAINEL
                    # SOMENTE SE ELE ESTIVER ABERTO
                    # ==========================================

                    painel = getattr(
                        topbar_atual,
                        "painel_notificacoes",
                        None,
                    )

                    atualizar_lista = getattr(
                        topbar_atual,
                        "atualizar_lista_notificacoes",
                        None,
                    )

                    if (
                        painel is not None
                        and painel.visible
                        and atualizar_lista is not None
                    ):

                        novas_notificacoes = (
                            await asyncio.to_thread(
                                listar_notificacoes
                            )
                        )

                        atualizar_lista(
                            novas_notificacoes
                        )

                    self._page.update()

            except asyncio.CancelledError:
                break

            except Exception as erro:

                print(
                    f"Erro ao atualizar notificações: {erro}"
                )

            await asyncio.sleep(5)