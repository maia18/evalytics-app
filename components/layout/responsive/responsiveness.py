import flet as ft
from typing import Callable, Optional
from components.layout.sidebar.sidebar_factory import criar_sidebar_desktop
from components.core.constants.constants import (
    LARGURA_BREAKPOINT_MOBILE,
    LARGURA_BREAKPOINT_DESKTOP,
    LARGURA_SIDEBAR_EXPANDIDA,
    LARGURA_SIDEBAR_COLAPSADA,
)

# Classifica a largura da janela em uma categoria de layout
def _categoria_layout(largura: float) -> str:
    if largura < LARGURA_BREAKPOINT_MOBILE:
        return "mobile"
    if largura < LARGURA_BREAKPOINT_DESKTOP:
        return "compacta"
    return "desktop"

def ajustar_responsividade(
    page: ft.Page,
    sidebar_desktop: ft.Control,
    topbar: ft.Control,
    fechar_sidebar: Callable[[], None],
    dark_mode: bool,
    mudar_tela: Optional[Callable[[str], None]],
) -> None:
    """
    Ajusta o layout da interface conforme a largura da janela.

    Evita reconstruir a sidebar quando a categoria de layout (mobile / compacta / desktop) não mudou desde o último ajuste, para não reconstruir widgets a cada pixel de redimensionamento.
    """
    categoria = _categoria_layout(page.width)

    if sidebar_desktop.data == categoria:
        return  # Nenhuma mudança de categoria: evita reconstrução desnecessária

    sidebar_desktop.data = categoria  # Cacheia a categoria atual no próprio controle

    if categoria == "mobile":
        sidebar_desktop.visible = False  # Oculta a sidebar de desktop
        sidebar_desktop.width = 0        # Remove seu preenchimento de largura
        topbar.menu_button.visible = True  # Habilita o botão 'hamburguer' mobile
    else:
        sidebar_desktop.visible = True     # Traz a sidebar de desktop de volta à vista
        topbar.menu_button.visible = False  # Esconde o botão de menu mobile
        fechar_sidebar()  # Força o fechamento da versão mobile, caso estivesse aberta

        # Ajuste adaptativo extra: menu diminui para modo ícone em telas médias
        sidebar_desktop.width = (
            LARGURA_SIDEBAR_EXPANDIDA if categoria == "desktop" else LARGURA_SIDEBAR_COLAPSADA
        )
        sidebar_desktop.content = criar_sidebar_desktop(
            dark_mode=dark_mode,
            mudar_tela=mudar_tela,
            collapsed=categoria == "compacta",
        ).content

    page.update()  # Atualiza a interface com os novos tamanhos