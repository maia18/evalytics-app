import flet as ft
from typing import Callable
from components.core.constants.constants import (
    TEXTO_PRINCIPAL, 
    SURFACE, 
    COR_PRIMARIA
)
from components.layout.topbar.topbar_utils import obter_icone_tema
from utils.services.location.location_service import obter_localizacao
from .core.notifications.topbar_notifications import criar_componentes_notificacoes

def criar_topbar_content(
    page: ft.Page,
    titulo: str,
    subtitulo: str,
    dark_mode: bool,
    cores: dict[str, str],
    menu_button: ft.IconButton,
    atualizar_tema: Callable[[], None],
    notificacoes_pendentes: int = 0,
) -> ft.Row:

    local_atual = obter_localizacao()
    icone_tema = obter_icone_tema(dark_mode)

    area_notificacoes, painel_notificacoes, badge_notificacoes, atualizar_lista = criar_componentes_notificacoes(page, cores)

    conteudo = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        controls=[
            ft.Row(
                spacing=10,
                controls=[
                    menu_button,
                    ft.Column(
                        spacing=0,
                        controls=[
                            ft.Text(titulo, size=20, weight="bold", color=cores[TEXTO_PRINCIPAL]),
                            ft.Text(subtitulo, size=12, color=ft.Colors.GREY),
                        ],
                    ),
                ],
            ),
   
            ft.Row(
                controls=[
                    ft.Container(
                        padding=10,
                        border_radius=8,
                        bgcolor=cores[SURFACE],
                        content=ft.Row(
                            spacing=6,
                            controls=[
                                ft.Icon(ft.Icons.LOCATION_ON_OUTLINED, size=18, color=COR_PRIMARIA),
                                ft.Text(local_atual, size=14, weight="w500", color=cores[TEXTO_PRINCIPAL]),
                            ],
                        ),
                    ),
                    ft.IconButton(
                        icon=icone_tema,
                        on_click=lambda e: atualizar_tema(),
                    ),
                    area_notificacoes,
                    ft.CircleAvatar(
                        radius=18,
                        color=cores[TEXTO_PRINCIPAL],
                        content=ft.Text("AC"),
                    ),
                ],
            ),
        ],
    )
    
    conteudo.badge_notificacoes = badge_notificacoes
    conteudo.painel_notificacoes = painel_notificacoes
    conteudo.atualizar_lista_notificacoes = atualizar_lista

    return conteudo