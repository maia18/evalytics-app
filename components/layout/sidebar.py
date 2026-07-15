import flet as ft

from components.layout.menu import MENU_ITEMS, MENU_ITEMS_COLLAPSED
from components.layout.menu_item import criar_item_menu, criar_botao_icon
from components.core.theme import AppColors # Importe o seu Design System

class Sidebar(ft.Container):
    
    """
    Sidebar reutilizável do sistema integrada ao Design System.
    """

    def __init__(self, dark_mode: bool, mudar_tela, collapsed=False,):
        super().__init__()

        self.dark_mode = dark_mode
        self.mudar_tela = mudar_tela
        self.collapsed = collapsed
        
        self.cores = AppColors.get(self.dark_mode) # Puxa as cores dinâmicas baseadas no tema atual

        self.bgcolor = self.cores["CARD"]
        self.padding = 20
        self.border = ft.Border(right=ft.BorderSide(1, self.cores["BORDA"]))

        self.width = 72 if collapsed else 250

        self.content = (self._criar_sidebar_colapsada() if collapsed  else self._criar_sidebar_content()
        )

    def _criar_sidebar_content(self):
        """Sidebar completa"""

        logo_container = ft.Container(
            content=ft.Row(
                spacing=10,
                controls=[
                    ft.Icon(
                        ft.Icons.ANALYTICS,
                        color=AppColors.PRIMARIA,
                        size=28,
                    ),
                    ft.Text(
                        "Evalytics",
                        size=18,
                        weight="bold",
                        color=self.cores["TEXTO_PRINCIPAL"],
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=15,
            height=60,
        )

        controles = [
            logo_container,
            ft.Divider(height=2),
        ]

        for icone, texto, rota in MENU_ITEMS:
            controles.append(
                criar_item_menu(
                    icone,
                    texto,
                    rota,
                    self.dark_mode,
                    self.cores["TEXTO_PRINCIPAL"],
                    self.mudar_tela,
                )
            )

        return ft.Column(
            controls=controles,
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
            expand=False,
        )

    def _criar_sidebar_colapsada(self):
        """Sidebar apenas com ícones"""

        controles = [
            ft.Container(
                content=ft.Icon(
                    ft.Icons.ANALYTICS,
                    color=AppColors.PRIMARIA,
                    size=28,
                ),
                padding=8,
                alignment=ft.Alignment.CENTER,
            ),
            ft.Divider(height=1),
        ]

        for icone, texto, rota in MENU_ITEMS_COLLAPSED:
            controles.append(
                criar_botao_icon(
                    icone,
                    texto,
                    rota,
                    self.dark_mode,
                    self.cores["TEXTO_PRINCIPAL"],
                    self.mudar_tela,
                )
            )

        controles.append(
            ft.Divider(height=1)
        )

        return ft.Column(
            controls=controles,
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.START,
        )