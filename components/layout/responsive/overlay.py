import flet as ft
from components.core.theme.theme import AppColors

def criar_overlay(fechar_sidebar_callback):
    return ft.Container(
        visible=False,
        expand=True,
        bgcolor=AppColors.OVERLAY_MODAL,
        on_click=lambda e: fechar_sidebar_callback(),
    )
