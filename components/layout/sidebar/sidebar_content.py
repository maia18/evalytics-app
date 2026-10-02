import flet as ft
from typing import Callable
from components.core.constants.constants import TEXTO_PRINCIPAL
from components.layout.sidebar.sidebar_logout import criar_botao_logout
from components.layout.sidebar.sidebar_logo import criar_logo
from components.layout.sidebar.sidebar_items import montar_botoes_menu
from components.widgets.menu.menu import MENU_ITEMS
from components.widgets.menu.menu_item import criar_item_menu

# Constrói a visualização padrão do menu, com logotipo completo e botões descritivos
def criar_sidebar_content(
    page,
    dark_mode: bool,
    mudar_tela: Callable[[str], None],
    cores: dict[str, str],
) -> ft.Column:
    
    controles: list[ft.Control] = [
        criar_logo(cores),        # Renderiza a versão em texto e ícone do logo do sistema
        ft.Divider(height=2),     # Separa o cabeçalho das rotas de navegação
    ]

    controles.extend(
        montar_botoes_menu(
            MENU_ITEMS,
            criar_item_menu,
            dark_mode,
            cores[TEXTO_PRINCIPAL],
            mudar_tela,
        )
    )
    
    controles.extend(
        [
            ft.Container(expand=True),

            ft.Divider(height=1),

            criar_botao_logout(
                page=page,
                dark_mode=dark_mode,
                cor_texto=cores[TEXTO_PRINCIPAL],
                mudar_tela=mudar_tela,
            ),
        ]
    )

    return ft.Column(
        controls=controles,
        spacing=0,                    # Mantém os botões colados uns nos outros
        expand=True,                 # Não força a coluna a ocupar mais espaço do que o necessário
    )