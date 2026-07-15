# core/theme.py
import flet as ft

class AppColors:
    
    # Cores fixas da marca
    PRIMARIA = "#F59E0B"
    OVERLAY_MODAL = "#00000088"
    
    @staticmethod
    def get(dark_mode: bool) -> dict:
        
        """Retorna o dicionário de cores baseado no tema atual."""
        
        return {
            "FUNDO": "#1E1E1E" if dark_mode else "#F9FAFB",
            "BORDA": "#3C3C3C" if dark_mode else "#E5E7EB",
            "CARD": "#2C2C2C" if dark_mode else "white",
            "TEXTO_PRINCIPAL": "white" if dark_mode else "black",
            "TEXTO_SECUNDARIO": "grey300" if dark_mode else "grey700",
            "HOVER": "#3C3C3C" if dark_mode else "#CCCCCC",
            "SURFACE": "#3C3C3C" if dark_mode else "#E5E7EB",
        }

def get_app_theme(dark_mode: bool) -> ft.Theme:
    
    """Configura o tema nativo do Flet."""
    
    tema = ft.Theme()
    tema.color_scheme_seed = AppColors.PRIMARIA
    return tema