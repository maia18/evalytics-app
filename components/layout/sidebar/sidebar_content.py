import flet as ft
from typing import Callable
from components.core.constants.constants import TEXTO_PRINCIPAL
from components.layout.sidebar.sidebar_logout import criar_botao_logout
from components.layout.sidebar.sidebar_logo import criar_logo
from components.layout.sidebar.sidebar_items import montar_botoes_menu
from components.widgets.menu.menu import MENU_ITEMS
from components.widgets.menu.menu_item import criar_item_menu

def criar_sidebar_content(
    page: ft.Page,
    dark_mode: bool,
    mudar_tela: Callable[[str], None],
    cores: dict[str, str],
) -> ft.Column:
    """Constrói a visualização padrão (expandida) da barra lateral do sistema."""

    # 1. Estrutura base da Sidebar
    controles: list[ft.Control] = [
        # Logo completo
        criar_logo(
            cores,
        ),

        # Separador
        ft.Divider(
            height=2,
        ),
    ]

    # 2. Construção da lista de navegação
    controles.extend(
        montar_botoes_menu(
            MENU_ITEMS,
            criar_item_menu,
            dark_mode,
            cores[TEXTO_PRINCIPAL],
            mudar_tela,
        )
    )

    # 3. Rodapé da Sidebar
    controles.extend(
        [
            # Ocupa o espaço restante e empurra o logout para baixo
            ft.Container(
                expand=True,
            ),

            ft.Divider(
                height=1,
            ),

            # Botão de logout
            criar_botao_logout(
                page=page,
                dark_mode=dark_mode,
                cor_texto=cores[TEXTO_PRINCIPAL],
                mudar_tela=mudar_tela,
            ),
        ]
    )

    # 4. Retorno do contêiner principal
    return ft.Column(
        controls=controles,
        spacing=0,
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )