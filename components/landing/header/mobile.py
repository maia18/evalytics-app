import flet as ft
from typing import Callable
from components.core.constants.constants import (
    COR_TEXTO_TITULO,
    COR_TEXTO_SECUNDARIO,
    COR_PRIMARIA,
)

def criar_menu_mobile(
    page: ft.Page, 
    mudar_tela: Callable[[str], None], 
    ir_para_recursos: Callable, 
    ir_para_sobre: Callable
) -> ft.Column:
    """Cria o menu de navegação mobile, incluindo abertura e fechamento do menu."""

    menu_mobile_aberto = False

    # =========================================================
    # BOTÕES DE CONTROLE
    # =========================================================

    btn_menu = ft.IconButton(
        icon=ft.Icons.MENU,
        icon_size=25,
        icon_color=COR_TEXTO_TITULO,
    )

    btn_fechar = ft.IconButton(
        icon=ft.Icons.CLOSE,
        icon_size=25,
        icon_color=COR_TEXTO_TITULO,
    )

    # =========================================================
    # CONTEÚDO DO MENU
    # =========================================================

    menu_mobile_conteudo = ft.Container(
        visible=False,
        padding=ft.Padding.only(
            left=20,
            right=20,
            bottom=20,
        ),
        content=ft.Column(
            spacing=4,
            controls=[
                
                # Recursos
                ft.TextButton(
                    "Recursos",
                    style=ft.ButtonStyle(
                        color=COR_TEXTO_SECUNDARIO,
                        alignment=ft.Alignment.CENTER_LEFT,
                    ),
                    on_click=ir_para_recursos,
                ),

                # Sobre
                ft.TextButton(
                    "Sobre",
                    style=ft.ButtonStyle(
                        color=COR_TEXTO_SECUNDARIO,
                        alignment=ft.Alignment.CENTER_LEFT,
                    ),
                    on_click=ir_para_sobre,
                ),

                # Login
                ft.TextButton(
                    "Entrar",
                    style=ft.ButtonStyle(
                        color=COR_PRIMARIA,
                        alignment=ft.Alignment.CENTER_LEFT,
                    ),
                    on_click=lambda e: mudar_tela("/login"),
                ),
            ],
        ),
    )

    # =========================================================
    # CONTROLE DO MENU
    # =========================================================

    async def alternar_menu_mobile(e):

        nonlocal menu_mobile_aberto
        menu_mobile_aberto = not menu_mobile_aberto
        menu_mobile_conteudo.visible = menu_mobile_aberto
        btn_menu.visible = not menu_mobile_aberto
        btn_fechar.visible = menu_mobile_aberto

        page.update()

    btn_menu.on_click = alternar_menu_mobile
    btn_fechar.on_click = alternar_menu_mobile

    btn_fechar.visible = False

    # =========================================================
    # COMPOSIÇÃO
    # =========================================================

    return ft.Column(
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.END,
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.END,
                controls=[
                    btn_menu,
                    btn_fechar,
                ],
            ),

            menu_mobile_conteudo,
        ],
    )