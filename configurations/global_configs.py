""" Importações """  
import os
import flet as ft

from configurations.config import * # Importa as configurações globais definidas em configurations/config.py

def configurar_aplicacao(page: ft.Page):
    
    """
    Aplica as configurações globais da aplicação.
    """
    
    page.title = APP_TITLE # Define o título da janela da aplicação
    
    # Define largura e altura da janela
    page.window.width = WINDOW_WIDTH
    page.window.height = WINDOW_HEIGHT
    
    page.theme_mode = ft.ThemeMode.LIGHT # Define o tema da aplicação (claro neste caso)

    page.padding = 0 # Remove qualquer espaçamento interno padrão da página

    page.bgcolor = ft.Colors.BLUE_GREY_50 # Define a cor de fundo da aplicação

    """ 
    Define o ícone da janela (logo da aplicação).
    O caminho é construído dinamicamente para funcionar em diferentes sistemas
    """
    page.window.icon = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),     # Caminho até a raiz do projeto
        "assets",                                       # Pasta onde está o ícone
        "imgs",
        "logo.ico"                                      # Nome do arquivo do ícone
    )