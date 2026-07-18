import flet as ft
from components.widgets.menu.menu import MENU_ITEMS
from components.widgets.menu.menu_item import criar_item_menu
from components.layout.sidebar.sidebar_logo import criar_logo
from components.core.constants.constants import *

# Sidebar completa
def criar_sidebar_content(dark_mode, mudar_tela, cores):
    
    controles = [
        criar_logo(cores),
        ft.Divider(height=2),
    ]

    for icone, texto, rota in MENU_ITEMS:
        controles.append(
            criar_item_menu(
                icone, texto, rota, dark_mode, cores[TEXTO_PRINCIPAL], mudar_tela
            )
        )

    return ft.Column(
        controls=controles,
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
        expand=False,
    )