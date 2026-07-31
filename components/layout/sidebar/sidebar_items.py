from typing import Callable, Iterable

import flet as ft

# Formato padrão de um item de menu: (ícone, texto, rota)
MenuItem = tuple[str, str, str]
MenuItemBuilder = Callable[[str, str, str, bool, str, Callable[[str], None]], ft.Control]


def montar_botoes_menu(
    items: Iterable[MenuItem],
    builder: MenuItemBuilder,
    dark_mode: bool,
    cor_texto: str,
    mudar_tela: Callable[[str], None],
) -> list[ft.Control]:
    """Constrói a lista de controles de menu aplicando `builder` a cada item.

    Compartilhado entre a sidebar completa e a sidebar colapsada, que diferem
    apenas na função construtora (`criar_item_menu` vs `criar_botao_icon`) e
    na lista de itens percorrida.
    """
    return [
        builder(icone, texto, rota, dark_mode, cor_texto, mudar_tela)
        for icone, texto, rota in items
    ]