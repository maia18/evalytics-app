from typing import Callable

import flet as ft

from utils.services.location_service import obter_localizacao
from components.layout.topbar.topbar_utils import obter_icone_tema
from components.core.constants.constants import TEXTO_PRINCIPAL, SURFACE, COR_PRIMARIA


def criar_topbar_content(
    titulo: str,
    subtitulo: str,
    dark_mode: bool,
    cores: dict[str, str],
    menu_button: ft.IconButton,
    atualizar_tema: Callable[[], None],
) -> ft.Row:
    """Constrói a disposição dos elementos internos da TopBar."""
    local_atual = obter_localizacao()  # Recupera a string de localização do serviço externo
    icone_tema = obter_icone_tema(dark_mode)

    return ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        controls=[
            # Lado esquerdo
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
            # Lado direito
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
                    ft.IconButton(icon=icone_tema, on_click=lambda e: atualizar_tema()),
                    ft.IconButton(icon=ft.Icons.NOTIFICATIONS_NONE),  # Decorativo/futuro para avisos
                    ft.CircleAvatar(radius=18, color=cores[TEXTO_PRINCIPAL], content=ft.Text("AC")),
                ],
            ),
        ],
    )