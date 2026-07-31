import flet as ft

from components.widgets.menu.menu import MENU_ITEMS
from components.widgets.menu.menu_item import criar_item_menu
from components.layout.sidebar.sidebar_logo import criar_logo
from components.layout.sidebar.sidebar_items import montar_botoes_menu
from components.core.constants.constants import TEXTO_PRINCIPAL
from typing import Callable


def criar_sidebar_content(dark_mode: bool, mudar_tela: Callable[[str], None], cores: dict[str, str]) -> ft.Column:
    """Constrói a visualização padrão do menu, com logotipo completo e botões descritivos."""
    controles: list[ft.Control] = [
        criar_logo(cores),        # Renderiza a versão em texto e ícone do logo do sistema
        ft.Divider(height=2),     # Separa o cabeçalho das rotas de navegação
    ]

    controles.extend(
        montar_botoes_menu(MENU_ITEMS, criar_item_menu, dark_mode, cores[TEXTO_PRINCIPAL], mudar_tela)
    )

    return ft.Column(
        controls=controles,
        spacing=0,                    # Mantém os botões colados uns nos outros
        scroll=ft.ScrollMode.AUTO,
        expand=False,                 # Não força a coluna a ocupar mais espaço do que o necessário
    )