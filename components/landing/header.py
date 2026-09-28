import flet as ft
from typing import Callable

from components.core.constants.constants import (
    COR_TEXTO_TITULO,
    COR_TEXTO_SECUNDARIO,
    COR_PRIMARIA,
)

def criar_logo() -> ft.Row:

    return ft.Row(
        spacing=10,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Image(
                src="imgs/logo.png",
                width=38,
                height=38,
                fit="CONTAIN",
            ),

            ft.Text(
                "Evalytics",
                size=20,
                weight=ft.FontWeight.BOLD,
                color=COR_TEXTO_TITULO,
            ),
        ],
    )


def criar_header(
    page: ft.Page,
    mudar_tela: Callable[[str], None],
    ir_para_recursos: Callable,
    ir_para_sobre: Callable,
) -> ft.ResponsiveRow:

    logo = criar_logo()

    # =========================================================
    # MENU DESKTOP
    # =========================================================

    btn_entrar = ft.TextButton(
        "Entrar",
        style=ft.ButtonStyle(
            color=COR_PRIMARIA,
        ),
        on_click=lambda e: mudar_tela("/login"),
    )

    menu_desktop = ft.Row(
        spacing=20,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.TextButton(
                "Recursos",
                style=ft.ButtonStyle(
                    color=COR_TEXTO_SECUNDARIO,
                ),
                on_click=ir_para_recursos,
            ),

            ft.TextButton(
                "Sobre",
                style=ft.ButtonStyle(
                    color=COR_TEXTO_SECUNDARIO,
                ),
                on_click=ir_para_sobre,
            ),

            btn_entrar,
        ],
    )

    # =========================================================
    # MENU MOBILE
    # =========================================================

    menu_mobile_aberto = False

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
                ft.TextButton(
                    "Recursos",
                    style=ft.ButtonStyle(
                        color=COR_TEXTO_SECUNDARIO,
                        alignment=ft.Alignment.CENTER_LEFT,
                    ),
                    on_click=ir_para_recursos,
                ),

                ft.TextButton(
                    "Sobre",
                    style=ft.ButtonStyle(
                        color=COR_TEXTO_SECUNDARIO,
                        alignment=ft.Alignment.CENTER_LEFT,
                    ),
                    on_click=ir_para_sobre,
                ),

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

    menu_mobile = ft.Column(
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

    # =========================================================
    # HEADER DESKTOP
    # =========================================================

    header_desktop = ft.Container(
        padding=ft.Padding.symmetric(
            horizontal=60,
            vertical=16,
        ),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                logo,
                menu_desktop,
            ],
        ),
    )

    # =========================================================
    # HEADER MOBILE
    # =========================================================

    header_mobile = ft.Container(
        padding=ft.Padding.symmetric(
            horizontal=20,
            vertical=15,
        ),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=[
                logo,
                menu_mobile,
            ],
        ),
    )

    # =========================================================
    # RESPONSIVIDADE
    # =========================================================

    return ft.ResponsiveRow(
        columns=12,
        controls=[
            ft.Container(
                col={
                    "xs": 12,
                    "sm": 12,
                    "md": 12,
                    "lg": 12,
                    "xl": 12,
                },
                content=ft.ResponsiveRow(
                    columns=12,
                    controls=[
                        ft.Container(
                            col={
                                "xs": 12,
                                "sm": 12,
                                "md": 0,
                                "lg": 0,
                                "xl": 0,
                            },
                            content=header_mobile,
                        ),

                        ft.Container(
                            col={
                                "xs": 0,
                                "sm": 0,
                                "md": 12,
                                "lg": 12,
                                "xl": 12,
                            },
                            content=header_desktop,
                        ),
                    ],
                ),
            ),
        ],
    )