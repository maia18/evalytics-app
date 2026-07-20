import os
import flet as ft

from components.core.constants.constants import *   # Importa as constantes definidas
from components.core.constants.texts import *       # Importa os textos

def configurar_aplicacao(page: ft.Page):
    
    page.title = APP_TITLE # Define o título da janela 
    
    page.window.width = WINDOW_WIDTH    # Largura da janela
    page.window.height = WINDOW_HEIGHT  # Altura da janela
    page.padding = 0                    # Remove espaçamentos internos padrões
    
    page.theme_mode = ft.ThemeMode.LIGHT    # Define o tema da página
    page.bgcolor = ft.Colors.BLUE_GREY_50   # Define a cor de fundo da aplicação

    page.window.icon = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "imgs", # Caminho             
        "logo.ico"                                                                     # Nome do ícone da janela
    )