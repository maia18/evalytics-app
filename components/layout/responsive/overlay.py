import flet as ft
from components.core.constants.constants import *

def criar_overlay(fechar_sidebar_callback):
    return ft.Container(
        visible=False,
        expand=True,
        bgcolor=OVERLAY_MODAL,
        on_click=lambda e: fechar_sidebar_callback(),
    )
