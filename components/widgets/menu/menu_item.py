from typing import Callable, Optional

import flet as ft

from components.widgets.menu.menu_button_base import criar_botao_menu_base


def criar_item_menu(
    icone: str,
    texto: str,
    rota: str,
    dark_mode: bool,
    cor_texto: str,
    mudar_tela: Optional[Callable[[str], None]],
) -> ft.Container:
    """Cria o botão de navegação tradicional: ícone à esquerda alinhado a um texto."""
    conteudo = ft.Row(
        spacing=12,
        controls=[
            ft.Icon(
                icone,
                size=20,  # Sutilmente menor que a versão colapsada (24)
                # Tom de cinza (mais escuro no claro, mais claro no escuro) para não
                # competir com o texto principal
                color=ft.Colors.GREY_700 if not dark_mode else ft.Colors.GREY_300,
            ),
            ft.Text(texto, size=14, weight="w500", color=cor_texto),
        ],
    )
    return criar_botao_menu_base(
        content=conteudo,
        rota=rota,
        dark_mode=dark_mode,
        mudar_tela=mudar_tela,
    )