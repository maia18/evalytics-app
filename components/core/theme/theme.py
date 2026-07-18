import flet as ft
from components.core.constants.constants import *

class AppColors:
    
    @staticmethod
    def get(dark_mode: bool) -> dict:
        
        return {
            FUNDO: FUNDO if dark_mode else COR_FUNDO,
            BORDA: BORDA if dark_mode else BORDA_NOT_DARKMODE,
            CARD: CARD if dark_mode else COR_CARD,
            TEXTO_PRINCIPAL: TEXTO_PRINCIPAL if dark_mode else COR_TEXTO_TITULO,
            TEXTO_SECUNDARIO: TEXTO_SECUNDARIO if dark_mode else COR_TEXTO_SECUNDARIO,
            HOVER: HOVER if dark_mode else COR_BORDA,
            SURFACE: SURFACE if dark_mode else COR_BORDA,
        }

def get_app_theme(dark_mode: bool) -> ft.Theme:
    
    """Configura o tema nativo do Flet."""
    
    tema = ft.Theme()
    tema.color_scheme_seed = COR_PRIMARIA
    return tema