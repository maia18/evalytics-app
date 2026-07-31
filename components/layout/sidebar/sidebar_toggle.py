import flet as ft
from typing import Callable
from components.core.constants.constants import LARGURA_LIMITE_TOGGLE_SIDEBAR

# Inverte o estado de visibilidade do menu mobile, acionando os callbacks informados
def toggle_sidebar(
    page: ft.Page,
    sidebar_mobile_aberta: bool,
    abrir_sidebar: Callable[[], None],
    fechar_sidebar: Callable[[], None],
) -> bool:
    
    # Cláusula de Guarda: Se a largura da tela atual for maior ou igual ao limite configurado, o sistema bloqueia o comportamento de menu gaveta, pois telas largas não precisam dele
    if page.width >= LARGURA_LIMITE_TOGGLE_SIDEBAR:
        return sidebar_mobile_aberta  # Bloqueia o comportamento em telas largas
    
    # Verifica o estado atual: se a sidebar já estiver aberta, executa o callback de fechamento e retorna False
    if sidebar_mobile_aberta:
        fechar_sidebar()
        return False

    # Se chegou aqui, significa que a sidebar estava fechada. Então ele abre e retorna True
    abrir_sidebar()
    return True