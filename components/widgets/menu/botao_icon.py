from typing import Callable, Optional

import flet as ft

from components.widgets.menu.menu_button_base import criar_botao_menu_base


def criar_botao_icon(
    icone: str,
    tooltip_text: str,
    rota: str,
    dark_mode: bool,
    cor_texto: str,
    mudar_tela: Optional[Callable[[str], None]],
) -> ft.Container:
    """Cria um botão compacto que exibe apenas um ícone.

    Ideal para a sidebar quando o menu está recolhido.
    """
    icone_control = ft.Icon(
        icone,
        color=cor_texto,
        size=24,
        tooltip=tooltip_text,  # Balão de dica, já que não há texto escrito no botão
    )
    return criar_botao_menu_base(
        content=icone_control,
        rota=rota,
        dark_mode=dark_mode,
        mudar_tela=mudar_tela,
        alignment=ft.Alignment(0, 0),  # Centraliza o ícone no container
        expand=True,  # Ocupa todo o espaço disponível no container de 45px
    )