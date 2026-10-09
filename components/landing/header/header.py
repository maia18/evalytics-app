import flet as ft
from typing import Callable
from components.landing.header.logo import criar_logo
from components.landing.header.desktop import criar_menu_desktop
from components.landing.header.mobile import criar_menu_mobile

def criar_header(
    page: ft.Page,
    mudar_tela: Callable[[str], None],
    ir_para_recursos: Callable,
    ir_para_sobre: Callable,
) -> ft.ResponsiveRow:
    """Cria o cabeçalho responsivo da Landing Page. """

    logo = criar_logo()

    menu_desktop = criar_menu_desktop(
        mudar_tela=mudar_tela,
        ir_para_recursos=ir_para_recursos,
        ir_para_sobre=ir_para_sobre,
    )

    menu_mobile = criar_menu_mobile(
        page=page,
        mudar_tela=mudar_tela,
        ir_para_recursos=ir_para_recursos,
        ir_para_sobre=ir_para_sobre,
    )

    # =========================================================
    # LAYOUT DESKTOP
    # =========================================================

    header_desktop = ft.Container(
        padding=ft.Padding.symmetric(
            horizontal=60,
            vertical=12,
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
    # LAYOUT MOBILE
    # =========================================================

    header_mobile = ft.Container(
        padding=ft.Padding.symmetric(
            horizontal=20,
            vertical=12,
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