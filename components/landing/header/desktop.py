import flet as ft
from typing import Callable

from components.core.constants.constants import (
    COR_TEXTO_SECUNDARIO,
    COR_PRIMARIA,
)

def criar_menu_desktop(mudar_tela: Callable[[str], None], ir_para_recursos: Callable, ir_para_sobre: Callable) -> ft.Row:
    """
    Cria o menu de navegação para dispositivos desktop.

    O componente exibe os principais atalhos da Landing Page, permitindo que o usuário:

        - Navegue até a seção de recursos;
        - Navegue até a seção sobre;
        - Acesse a tela de login.
    """

    return ft.Row(
        spacing=20, # Espaçamento horizontal entre os itens do menu.
        vertical_alignment=ft.CrossAxisAlignment.CENTER, # Mantém todos os botões alinhados verticalmente.

        controls=[

            # =================================================
            # LINK: RECURSOS
            # =================================================
            
            # Realiza a navegação interna até a seção de funcionalidades da Landing Page.
            ft.TextButton(
                "Recursos",
                style=ft.ButtonStyle(
                    color=COR_TEXTO_SECUNDARIO,
                ),
                on_click=ir_para_recursos,
            ),

            # =================================================
            # LINK: SOBRE
            # =================================================
            
            # Realiza a navegação interna até a seção institucional da plataforma.
            ft.TextButton(
                "Sobre",
                style=ft.ButtonStyle(
                    color=COR_TEXTO_SECUNDARIO,
                ),
                on_click=ir_para_sobre,
            ),

            # =================================================
            # LINK: LOGIN
            # =================================================
            
            # Direciona o usuário para a área autenticada da aplicação através da tela de login.
            ft.TextButton(
                "Entrar",
                style=ft.ButtonStyle(
                    color=COR_PRIMARIA,
                ),
                on_click=lambda e: mudar_tela("/login"),
            ),
        ],
    )