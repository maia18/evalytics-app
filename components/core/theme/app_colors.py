from components.core.constants.constants import (
    COR_PRIMARIA,
    COR_FUNDO,
    FUNDO,
    BORDA,
    BORDA_NOT_DARKMODE,
    COR_CARD,
    CARD,
    COR_CARD_SECUNDARIO,
    CARD_SECUNDARIO,
    COR_TEXTO_TITULO,
    TEXTO_PRINCIPAL,
    COR_TEXTO_SECUNDARIO,
    TEXTO_SECUNDARIO,
    COR_TEXTO_MUTED,
    TEXTO_MUTED,
    HOVER,
    HOVER_CLARO,
    SURFACE,
    SURFACE_CLARO,
    SUCESSO,
    PERIGO,
    AVISO,
)

class AppColors:
    """
    Classe utilitária responsável por fornecer a paleta de cores correspondente ao tema atual.
        As chaves do dicionário são identificadores semânticos.
            Os valores mudam de acordo com o modo claro/escuro.
    """

    @staticmethod
    def get(dark_mode: bool) -> dict[str, str]:
        """Retorna a paleta de cores correspondente ao tema atual."""
        
        return {
            # Marca
            COR_PRIMARIA: COR_PRIMARIA,
            
            # Fundos
            FUNDO: FUNDO if dark_mode else COR_FUNDO,
            
            # Cards / superfícies
            CARD: CARD if dark_mode else COR_CARD,
            CARD_SECUNDARIO: CARD_SECUNDARIO if dark_mode else COR_CARD_SECUNDARIO,
            
            # Bordas
            BORDA: BORDA if dark_mode else BORDA_NOT_DARKMODE,
            
            # Textos
            TEXTO_PRINCIPAL: TEXTO_PRINCIPAL if dark_mode else COR_TEXTO_TITULO,
            TEXTO_SECUNDARIO: TEXTO_SECUNDARIO if dark_mode else COR_TEXTO_SECUNDARIO,
            TEXTO_MUTED: TEXTO_MUTED if dark_mode else COR_TEXTO_MUTED,
            
            # Interação
            HOVER: HOVER if dark_mode else HOVER_CLARO,
            SURFACE: SURFACE if dark_mode else SURFACE_CLARO,
            
            # Estados
            SUCESSO: SUCESSO,
            PERIGO: PERIGO,
            AVISO: AVISO,
        }