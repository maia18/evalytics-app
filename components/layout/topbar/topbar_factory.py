from typing import Callable

from components.layout.topbar.topbar import TopBar


def criar_topbar(
    titulo: str,
    subtitulo: str,
    dark_mode: bool,
    toggle_sidebar: Callable[[], None],
    atualizar_tema: Callable[[], None],
) -> TopBar:
    """Padrão Factory: instancia o objeto TopBar repassando as dependências de forma limpa."""
    return TopBar(
        titulo_pagina=titulo,
        subtitulo=subtitulo,
        dark_mode=dark_mode,
        toggle_sidebar=toggle_sidebar,
        atualizar_tema=atualizar_tema,
    )