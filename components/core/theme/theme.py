import flet as ft
from components.core.constants.constants import * # constantes do projeto (como identificadores de chaves e códigos hexadecimais das cores)

# Classe utilitária para gerenciar as paletas de cores da aplicação.
class AppColors:
    
    @staticmethod
    def get(dark_mode: bool) -> dict:
        
        """
        Retorna um dicionário com a paleta de cores adequada de acordo com o tema atual.

        - Constrói e retorna o dicionário de cores usando operadores ternários.
        - A lógica é: CHAVE: COR_MODO_ESCURO if dark_mode else COR_MODO_CLARO
        - Obs: As constantes (ex: FUNDO, BORDA) estão atuando como chaves do dicionário e também como os valores de cor para o modo escuro.
        """
        
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
    
    """Configura e retorna o objeto de tema nativo do Flet."""
    
    tema = ft.Theme() # Inicializa um novo objeto de tema do Flet
    tema.color_scheme_seed = COR_PRIMARIA # Define a cor semente (seed) do esquema de cores.
    return tema # Retorna o tema configurado para ser aplicado na página (page.theme)