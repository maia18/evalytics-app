import flet as ft
from typing import Callable

from components.core.constants.constants import (
    TEXTO_PRINCIPAL,
    SURFACE,
    COR_PRIMARIA,
)

from components.layout.topbar.topbar_utils import (
    obter_icone_tema,
)

from utils.services.location_service import (
    obter_localizacao,
)


# ==========================================================
# CONSTRÓI O CONTEÚDO DA TOPBAR
# ==========================================================

def criar_topbar_content(
    titulo: str,
    subtitulo: str,
    dark_mode: bool,
    cores: dict[str, str],
    menu_button: ft.IconButton,
    atualizar_tema: Callable[[], None],
    notificacoes_pendentes: int = 0,
) -> ft.Row:

    local_atual = obter_localizacao()

    icone_tema = obter_icone_tema(
        dark_mode
    )

    # ======================================================
    # BADGE DE NOTIFICAÇÕES
    # ======================================================

    badge_notificacoes = ft.Container(
        width=16,
        height=16,
        right=1,
        top=1,
        bgcolor="#EF4444",
        border_radius=8,
        alignment=ft.Alignment.CENTER,
        visible=notificacoes_pendentes > 0,
        content=ft.Text(
            str(notificacoes_pendentes),
            size=9,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE,
        ),
    )

    # ======================================================
    # PAINEL DE NOTIFICAÇÕES
    # ======================================================

    painel_notificacoes = ft.Container(
        width=320,
        visible=False,

        # Posição dentro do Page.overlay
        top=66,
        right=66,

        bgcolor=cores[SURFACE],

        border_radius=12,

        padding=0,

        shadow=ft.BoxShadow(
            blur_radius=20,
            spread_radius=1,
            color="#33000000",
        ),
    )

    # ======================================================
    # BOTÃO DE NOTIFICAÇÕES
    # ======================================================

    botao_notificacoes = ft.IconButton(
        icon=ft.Icons.NOTIFICATIONS_NONE,
        tooltip="Notificações",
    )

    # ======================================================
    # FECHAR PAINEL
    # ======================================================

    def fechar_painel(e=None):

        painel_notificacoes.visible = False

        botao_notificacoes.icon = (
            ft.Icons.NOTIFICATIONS_NONE
        )

        painel_notificacoes.update()

    # ======================================================
    # ABRIR / FECHAR PAINEL
    # ======================================================

    def alternar_painel(e=None):

        painel_notificacoes.visible = (
            not painel_notificacoes.visible
        )

        botao_notificacoes.icon = (
            ft.Icons.NOTIFICATIONS
            if painel_notificacoes.visible
            else ft.Icons.NOTIFICATIONS_NONE
        )

        painel_notificacoes.update()

    botao_notificacoes.on_click = (
        alternar_painel
    )

    # ======================================================
    # MARCAR COMO LIDAS
    # ======================================================

    def marcar_como_lidas(e=None):

        badge_notificacoes.visible = False

        badge_notificacoes.content = ft.Text(
            "0",
            size=9,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE,
        )

        painel_notificacoes.visible = False

        botao_notificacoes.icon = (
            ft.Icons.NOTIFICATIONS_NONE
        )

        painel_notificacoes.update()
        badge_notificacoes.update()

    # ======================================================
    # NOTIFICAÇÕES DE TESTE
    # ======================================================

    notificacoes = [
        {
            "icone": ft.Icons.RATE_REVIEW_OUTLINED,
            "titulo": "Nova avaliação registrada",
            "descricao": "Uma nova avaliação foi concluída.",
            "tempo": "há 5 minutos",
        },
        {
            "icone": ft.Icons.TUNE_OUTLINED,
            "titulo": "Novo indicador cadastrado",
            "descricao": "Um novo indicador está disponível.",
            "tempo": "há 2 horas",
        },
        {
            "icone": ft.Icons.SCHOOL_OUTLINED,
            "titulo": "Curso atualizado",
            "descricao": "Informações de um curso foram alteradas.",
            "tempo": "ontem",
        },
    ]

    itens_notificacoes = []

    for notificacao in notificacoes:

        itens_notificacoes.append(
            ft.Container(
                padding=12,
                content=ft.Row(
                    spacing=12,
                    vertical_alignment=(
                        ft.CrossAxisAlignment.START
                    ),
                    controls=[
                        # Ícone
                        ft.Container(
                            width=34,
                            height=34,
                            border_radius=8,
                            bgcolor=cores[SURFACE],
                            alignment=ft.Alignment.CENTER,
                            content=ft.Icon(
                                notificacao["icone"],
                                size=18,
                                color=COR_PRIMARIA,
                            ),
                        ),

                        # Texto
                        ft.Column(
                            spacing=2,
                            expand=True,
                            controls=[
                                ft.Text(
                                    notificacao["titulo"],
                                    size=13,
                                    weight=ft.FontWeight.BOLD,
                                    color=cores[
                                        TEXTO_PRINCIPAL
                                    ],
                                ),

                                ft.Text(
                                    notificacao["descricao"],
                                    size=11,
                                    color=ft.Colors.GREY,
                                ),

                                ft.Text(
                                    notificacao["tempo"],
                                    size=10,
                                    color=ft.Colors.GREY,
                                ),
                            ],
                        ),
                    ],
                ),
            )
        )

    # ======================================================
    # CONTEÚDO DO PAINEL
    # ======================================================

    painel_notificacoes.content = ft.Column(
        spacing=0,
        controls=[
            # ------------------------------------------------
            # Cabeçalho
            # ------------------------------------------------

            ft.Container(
                padding=16,
                content=ft.Row(
                    alignment=(
                        ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    controls=[
                        ft.Text(
                            "Notificações",
                            size=15,
                            weight=ft.FontWeight.BOLD,
                            color=cores[
                                TEXTO_PRINCIPAL
                            ],
                        ),

                        ft.IconButton(
                            icon=ft.Icons.CLOSE,
                            icon_size=18,
                            tooltip="Fechar",
                            on_click=fechar_painel,
                        ),
                    ],
                ),
            ),

            ft.Divider(
                height=1
            ),

            # ------------------------------------------------
            # Lista
            # ------------------------------------------------

            ft.Column(
                spacing=0,
                controls=itens_notificacoes,
            ),

            ft.Divider(
                height=1
            ),

            # ------------------------------------------------
            # Rodapé
            # ------------------------------------------------

            ft.Container(
                padding=12,
                alignment=ft.Alignment.CENTER,
                content=ft.TextButton(
                    "Marcar como lidas",
                    on_click=marcar_como_lidas,
                ),
            ),
        ],
    )

    # ======================================================
    # ÁREA DA CAMPainha
    # ======================================================

    area_notificacoes = ft.Stack(
        width=40,
        height=40,
        clip_behavior=ft.ClipBehavior.NONE,
        controls=[
            botao_notificacoes,
            badge_notificacoes,
        ],
    )

    # ======================================================
    # LAYOUT PRINCIPAL DA TOPBAR
    # ======================================================

    conteudo = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        controls=[
            # ==================================================
            # LADO ESQUERDO
            # ==================================================

            ft.Row(
                spacing=10,
                controls=[
                    menu_button,

                    ft.Column(
                        spacing=0,
                        controls=[
                            ft.Text(
                                titulo,
                                size=20,
                                weight="bold",
                                color=cores[
                                    TEXTO_PRINCIPAL
                                ],
                            ),

                            ft.Text(
                                subtitulo,
                                size=12,
                                color=ft.Colors.GREY,
                            ),
                        ],
                    ),
                ],
            ),

            # ==================================================
            # LADO DIREITO
            # ==================================================

            ft.Row(
                controls=[
                    # ------------------------------------------
                    # Localização
                    # ------------------------------------------

                    ft.Container(
                        padding=10,
                        border_radius=8,
                        bgcolor=cores[SURFACE],
                        content=ft.Row(
                            spacing=6,
                            controls=[
                                ft.Icon(
                                    ft.Icons.LOCATION_ON_OUTLINED,
                                    size=18,
                                    color=COR_PRIMARIA,
                                ),

                                ft.Text(
                                    local_atual,
                                    size=14,
                                    weight="w500",
                                    color=cores[
                                        TEXTO_PRINCIPAL
                                    ],
                                ),
                            ],
                        ),
                    ),

                    # ------------------------------------------
                    # Tema
                    # ------------------------------------------

                    ft.IconButton(
                        icon=icone_tema,
                        on_click=lambda e: atualizar_tema(),
                    ),

                    # ------------------------------------------
                    # Notificações
                    # ------------------------------------------

                    area_notificacoes,

                    # ------------------------------------------
                    # Avatar
                    # ------------------------------------------

                    ft.CircleAvatar(
                        radius=18,
                        color=cores[
                            TEXTO_PRINCIPAL
                        ],
                        content=ft.Text(
                            "AC"
                        ),
                    ),
                ],
            ),
        ],
    )

    # ======================================================
    # REFERÊNCIAS PARA A CLASSE TOPBAR
    # ======================================================

    conteudo.badge_notificacoes = (
        badge_notificacoes
    )

    conteudo.painel_notificacoes = (
        painel_notificacoes
    )

    return conteudo