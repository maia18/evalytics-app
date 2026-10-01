import flet as ft
from typing import Callable

# Componentes especializados do Header
from components.landing.header.logo import criar_logo
from components.landing.header.desktop import criar_menu_desktop
from components.landing.header.mobile import criar_menu_mobile

def criar_header(
    page: ft.Page, 
    mudar_tela: Callable[[str], None], 
    ir_para_recursos: Callable, 
    ir_para_sobre: Callable
) -> ft.ResponsiveRow:
    """
    Cria o cabeçalho responsivo da Landing Page.

    Este componente atua como uma camada de composição, reunindo os elementos responsáveis pela identidade visual e pela navegação da aplicação.

    Estrutura:

        - Logo da plataforma;
        - Menu Desktop;
        - Menu Mobile;
        - Controle de exibição por tamanho de tela.

    Responsabilidades:

        - Montar os componentes do Header;
        - Aplicar os layouts Desktop e Mobile;
        - Controlar qual versão será exibida conforme o breakpoint da tela.
    """

    # =========================================================
    # COMPONENTES BASE
    # =========================================================
    
    # Cada elemento possui sua própria responsabilidade e implementação em módulos separados.

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
    
    ''' 
    Estrutura utilizada em tablets maiores e desktops.
        Layout:
            [ Logo ] ---------------- [ Menu ]
    '''
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
    # LAYOUT MOBILE
    # =========================================================
    
    '''
    Estrutura otimizada para smartphones.
        Layout:
            [ Logo ] [ Menu Hamburguer ]
    '''
    header_mobile = ft.Container(
        padding=ft.Padding.symmetric(
            horizontal=20,
            vertical=15,
        ),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

            # Permite expansão vertical do menu sem comprometer o alinhamento.
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
    
    '''
    Breakpoints utilizados:
    
        xs / sm  -> Mobile
        md / lg / xl -> Desktop
    
    A estratégia adotada consiste em manter os dois layouts disponíveis e controlar sua exibição através das colunas do ResponsiveRow.
    '''
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

                        # =====================================
                        # HEADER MOBILE
                        # =====================================
                        
                        # Visível apenas em telas pequenas.
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

                        # =====================================
                        # HEADER DESKTOP
                        # =====================================
                        
                        # Visível apenas em telas médias ou superiores.
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