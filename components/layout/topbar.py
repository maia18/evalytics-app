import flet as ft
from utils.services.location_service import obter_localizacao
from components.core.theme import AppColors # Importe o seu Design System

class TopBar(ft.Container):
    def __init__(
        self,
        titulo_pagina: str,
        subtitulo: str,
        dark_mode: bool,
        toggle_sidebar,
        atualizar_tema,
    ):
        super().__init__()

        self.titulo_pagina = titulo_pagina
        self.subtitulo = subtitulo
        self.dark_mode = dark_mode
        self._toggle_sidebar = toggle_sidebar
        self._atualizar_tema = atualizar_tema

        # Puxa as cores diretamente do Design System
        self.cores = AppColors.get(self.dark_mode)

        self.menu_button = ft.IconButton(
            icon=ft.Icons.MENU,
            on_click=lambda e: self._toggle_sidebar(),
        )

        self.bgcolor = self.cores["CARD"]
        self.padding = 20
        self.border = ft.Border(bottom=ft.BorderSide(1, self.cores["BORDA"]))
        self.content = self._criar_topbar_content()

    def _criar_topbar_content(self):
        local_atual = obter_localizacao()
        icone_tema = ft.Icons.LIGHT_MODE_OUTLINED if self.dark_mode else ft.Icons.DARK_MODE_OUTLINED

        return ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row(
                    spacing=10,
                    controls=[
                        self.menu_button,
                        ft.Column(
                            spacing=0,
                            controls=[
                                ft.Text(self.titulo_pagina, size=20, weight="bold", color=self.cores["TEXTO_PRINCIPAL"]),
                                ft.Text(self.subtitulo, size=12, color="grey"),
                            ],
                        ),
                    ],
                ),
                ft.Row(
                    controls=[
                        ft.Container(
                            padding=10,
                            border_radius=8,
                            bgcolor=self.cores["SURFACE"],
                            content=ft.Row(
                                spacing=6,
                                controls=[
                                    ft.Icon(ft.Icons.LOCATION_ON_OUTLINED, size=18, color=AppColors.PRIMARIA),
                                    ft.Text(local_atual, size=14, weight="w500", color=self.cores["TEXTO_PRINCIPAL"]),
                                ],
                            ),
                        ),
                        ft.IconButton(icon=icone_tema, on_click=lambda e: self._atualizar_tema()),
                        ft.IconButton(icon=ft.Icons.NOTIFICATIONS_NONE),
                        ft.CircleAvatar(radius=18, bgcolor=AppColors.PRIMARIA, content=ft.Text("AC")),
                    ],
                ),
            ],
        )