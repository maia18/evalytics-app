import flet as ft
from components.core.theme.theme import AppColors, get_app_theme # configurações customizadas de cores e tema do projeto

# Configura o tema visual da aplicação (cores, fontes, etc.) na página do Flet.
def configurar_tema(page: ft.Page, dark_mode: bool):
    page.theme = get_app_theme(dark_mode) # Obtém e define as configurações detalhadas do tema (como botões, textos, etc.) usando a função customizada do seu projeto
    
    ''' 
    Define o modo de tema nativo do Flet, usando um operador ternário
    Se dark_mode for True, usa ft.ThemeMode.DARK. Caso contrário, usa ft.ThemeMode.LIGHT
    '''
    page.theme_mode = ft.ThemeMode.DARK if dark_mode else ft.ThemeMode.LIGHT
    
    '''
    Retorna o esquema de cores correspondente ao tema atual
    Isso é útil para aplicar cores específicas manualmente em outros componentes do app
    '''
    return AppColors.get(dark_mode)