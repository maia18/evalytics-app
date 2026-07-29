import flet as ft
from typing import Callable
from components.core.constants.constants import OVERLAY_MODAL

# Cria uma camada de sobreposição (overlay) escura para destacar a sidebar mobile
def criar_overlay(fechar_sidebar_callback: Callable[[], None]) -> ft.Container:
    return ft.Container(
        visible=False,  # Inicia invisível até que a sidebar seja aberta
        expand=True,    # Ocupa 100% da tela disponível
        bgcolor=OVERLAY_MODAL,  # Cor de fundo transparente definida nas constantes
        on_click=lambda e: fechar_sidebar_callback(),  # Fecha a sidebar mobile ao clicar fora dela
    )