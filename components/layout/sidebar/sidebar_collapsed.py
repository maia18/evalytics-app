import flet as ft
from typing import Callable
from components.core.constants.constants import TEXTO_PRINCIPAL
from components.layout.sidebar.sidebar_logo import criar_logo
from components.layout.sidebar.sidebar_items import montar_botoes_menu
from components.widgets.menu.menu import MENU_ITEMS_COLLAPSED
from components.widgets.menu.botao_icon import criar_botao_icon

# Constrói os elementos do menu lateral focado apenas em ícones
def criar_sidebar_colapsada(dark_mode: bool, mudar_tela: Callable[[str], None], cores: dict[str, str]) -> ft.Column:
    controles: list[ft.Control] = [
        criar_logo(cores, compact=True),  # Versão do logo que só mostra o ícone
        ft.Divider(height=1),
    ]

    controles.extend(
        montar_botoes_menu(MENU_ITEMS_COLLAPSED, criar_botao_icon, dark_mode, cores[TEXTO_PRINCIPAL], mudar_tela)
    )

    controles.append(ft.Divider(height=1))

    return ft.Column(
        controls=controles,
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
        alignment=ft.MainAxisAlignment.START,
    )