from components.layout.topbar.topbar import TopBar

def criar_topbar(titulo, subtitulo, dark_mode, toggle_sidebar, atualizar_tema):
    return TopBar(
        titulo_pagina=titulo,
        subtitulo=subtitulo,
        dark_mode=dark_mode,
        toggle_sidebar=toggle_sidebar,
        atualizar_tema=atualizar_tema
    )
