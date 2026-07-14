# ==========================================
# components/layout/responsive_layout.py
# Layout principal da aplicação
# ==========================================

import flet as ft

from components.layout.sidebar import Sidebar
from components.layout.topbar import TopBar

from components.theme.theme import get_theme


class ResponsiveLayout:

    MOBILE_BREAKPOINT = 700
    TABLET_BREAKPOINT = 1100

    SIDEBAR_WIDTH = 250
    SIDEBAR_COLLAPSED_WIDTH = 72

    def __init__(
        self,
        page: ft.Page,
        titulo_pagina: str,
        subtitulo: str = "",
        mudar_tela=None,
    ):

        self.page = page

        self.titulo = titulo_pagina
        self.subtitulo = subtitulo

        self.mudar_tela = mudar_tela

        self.dark_mode = getattr(
            page,
            "is_dark_mode",
            False,
        )

        self.theme = get_theme(self.dark_mode)

        self.route = ""

        self.sidebar_mobile_open = False

        self.content = ft.Container(expand=True)

        self._create_components()

    # ---------------------------------------------------

    def _create_components(self):

        self.overlay = ft.Container(

            visible=False,

            expand=True,

            bgcolor=self.theme.colors.overlay,

            on_click=self.close_mobile_sidebar,

        )

        self.sidebar_mobile = ft.Container(

            left=-270,

            top=0,

            bottom=0,

            width=self.SIDEBAR_WIDTH,

            animate_position=ft.Animation(
                250,
                ft.AnimationCurve.EASE_OUT,
            ),

        )

        self.sidebar_desktop = ft.Container()

        self.topbar = TopBar(

            page=self.page,

            theme=self.theme,

            title=self.titulo,

            subtitle=self.subtitulo,

            dark_mode=self.dark_mode,

            on_menu=self.toggle_sidebar,

            on_toggle_theme=self.toggle_theme,

        )

    # ---------------------------------------------------

    def toggle_theme(self, e=None):

        self.dark_mode = not self.dark_mode

        self.page.is_dark_mode = self.dark_mode

        self.page.theme_mode = (

            ft.ThemeMode.DARK

            if self.dark_mode

            else ft.ThemeMode.LIGHT

        )

        if self.mudar_tela:

            self.mudar_tela(self.route)

    # ---------------------------------------------------

    def toggle_sidebar(self, e=None):

        if self.sidebar_mobile_open:

            self.close_mobile_sidebar()

        else:

            self.open_mobile_sidebar()

    # ---------------------------------------------------

    def open_mobile_sidebar(self):

        self.sidebar_mobile_open = True

        self.sidebar_mobile.left = 0

        self.overlay.visible = True

        self.page.update()

    # ---------------------------------------------------

    def close_mobile_sidebar(self, e=None):

        self.sidebar_mobile_open = False

        self.sidebar_mobile.left = -270

        self.overlay.visible = False

        self.page.update()

    # ---------------------------------------------------

    def add_content(self, control):

        self.content.content = control

    # ---------------------------------------------------

    def update_layout(self, e=None):

        width = self.page.width

        if width < self.MOBILE_BREAKPOINT:

            self.sidebar_desktop.visible = False

            self.topbar.on_menu = self.toggle_sidebar

            self.sidebar_mobile.content = Sidebar(

                theme=self.theme,

                collapsed=False,

                on_navigate=self.mudar_tela,

                current_route=self.route,

            )

            return

        self.close_mobile_sidebar()

        self.sidebar_desktop.visible = True

        collapsed = width < self.TABLET_BREAKPOINT

        self.sidebar_desktop.width = (

            self.SIDEBAR_COLLAPSED_WIDTH

            if collapsed

            else self.SIDEBAR_WIDTH

        )

        self.sidebar_desktop.content = Sidebar(

            theme=self.theme,

            collapsed=collapsed,

            on_navigate=self.mudar_tela,

            current_route=self.route,

        )

        self.page.update()

    # ---------------------------------------------------

    def create_view(self, route: str):

        self.route = route

        self.page.on_resize = self.update_layout

        self.update_layout()

        return ft.View(

            route=route,

            padding=0,

            bgcolor=self.theme.colors.background,

            controls=[

                ft.Stack(

                    expand=True,

                    controls=[

                        ft.Row(

                            expand=True,

                            spacing=0,

                            controls=[

                                self.sidebar_desktop,

                                ft.Column(

                                    expand=True,

                                    spacing=0,

                                    controls=[

                                        self.topbar,

                                        ft.Container(

                                            expand=True,

                                            padding=self.theme.spacing.XL,

                                            content=self.content,

                                        ),

                                    ],

                                ),

                            ],

                        ),

                        self.overlay,

                        self.sidebar_mobile,

                    ],

                )

            ],

        )