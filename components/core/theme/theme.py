import flet as ft
from components.core.constants.constants import COR_PRIMARIA

def get_app_theme(dark_mode: bool) -> ft.Theme:
    """
    Configura o tema nativo do Flet.
        A cor primária do Evalytics é utilizada como seed do Material Design 3.
    """
    tema = ft.Theme()
    
    # Define a cor base para geração automática da paleta do Material 3
    tema.color_scheme_seed = COR_PRIMARIA
    
    return tema