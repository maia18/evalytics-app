from typing import Callable

import flet as ft

# Largura acima da qual o toggle da sidebar mobile é ignorado (a UI já é
# tratada como "larga" o suficiente para não precisar de menu-gaveta).
#
# ATENÇÃO: este valor (900) é diferente do breakpoint mobile usado em
# responsiveness.py (700). Isso cria uma faixa de 700-900px onde a sidebar
# desktop já está visível, mas o toggle mobile ainda pode ser acionado.
# Mantido como estava para não alterar comportamento sem validação; considerar
# unificar os breakpoints numa próxima revisão.
LARGURA_LIMITE_TOGGLE_SIDEBAR = 900


def toggle_sidebar(
    page: ft.Page,
    sidebar_mobile_aberta: bool,
    abrir_sidebar: Callable[[], None],
    fechar_sidebar: Callable[[], None],
) -> bool:
    """Inverte o estado de visibilidade do menu mobile, acionando os callbacks informados."""
    if page.width >= LARGURA_LIMITE_TOGGLE_SIDEBAR:
        return sidebar_mobile_aberta  # Bloqueia o comportamento em telas largas

    if sidebar_mobile_aberta:
        fechar_sidebar()
        return False

    abrir_sidebar()
    return True