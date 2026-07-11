import os
import flet as ft

from configurations.config import *

def configurar_aplicacao(page: ft.Page):
    """Aplica as configurações globais da aplicação."""
    
    page.title = APP_TITLE

    page.window.width = WINDOW_WIDTH
    page.window.height = WINDOW_HEIGHT
    
    page.theme_mode = ft.ThemeMode.LIGHT

    page.padding = 0

    page.bgcolor = ft.Colors.BLUE_GREY_50

    page.window.icon = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "logo.ico")