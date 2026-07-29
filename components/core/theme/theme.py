import flet as ft
from components.core.constants.constants import (
    COR_PRIMARIA,
    COR_FUNDO,
    FUNDO,
    COR_BORDA,
    BORDA,
    BORDA_NOT_DARKMODE,
    COR_CARD,
    CARD,
    COR_TEXTO_TITULO,
    TEXTO_PRINCIPAL,
    COR_TEXTO_SECUNDARIO,
    TEXTO_SECUNDARIO,
    HOVER,
    SURFACE,
)

# Classe utilitária para gerenciar as paletas de cores da aplicação
class AppColors:
    
    # @staticmethod permite invocar o método direto pela classe (AppColors.get(True)), sem precisar instanciá-la (AppColors().get(True)).
    @staticmethod
    def get(dark_mode: bool) -> dict[str, str]:
        """
        Retorna a paleta de cores adequada de acordo com o tema atual.
        Observação de design: as chaves deste dicionário reutilizam as constantes de cor do MODO ESCURO (ex.: FUNDO, BORDA) como identificadores semânticos (ex.: "cor de fundo", "cor de borda").
            A chave representa o CONCEITO da cor, não necessariamente o valor retornado — o valor varia conforme `dark_mode`. 
            Isso é histórico do projeto; ao consumir este dicionário, trate as chaves como identificadores, não como cores literais do modo escuro.
        """
        
        # A lógica usa operadores ternários do Python (condicionais em uma linha) para montar um dicionário. Se 'dark_mode' for True, ele mapeia a chave para a constante do tema escuro, caso contrário, para a constante do tema claro.
        return {
            FUNDO: FUNDO if dark_mode else COR_FUNDO,
            BORDA: BORDA if dark_mode else BORDA_NOT_DARKMODE,
            CARD: CARD if dark_mode else COR_CARD,
            TEXTO_PRINCIPAL: TEXTO_PRINCIPAL if dark_mode else COR_TEXTO_TITULO,
            TEXTO_SECUNDARIO: TEXTO_SECUNDARIO if dark_mode else COR_TEXTO_SECUNDARIO,
            HOVER: HOVER if dark_mode else COR_BORDA,
            SURFACE: SURFACE if dark_mode else COR_BORDA,
        }

# Configura e retorna o objeto de tema nativo do Flet
def get_app_theme(dark_mode: bool) -> ft.Theme:
    """
    O parâmetro `dark_mode` é recebido para manter a assinatura consistente com o restante da API de temas, mesmo não sendo usado diretamente aqui (a cor semente é a mesma em ambos os temas; quem alterna claro/escuro é `page.theme_mode`, definido em `configurar_tema`).
    """
    tema = ft.Theme() # Instancia o objeto principal de tema do Flet.
    tema.color_scheme_seed = COR_PRIMARIA # Define a 'color_scheme_seed'. Com isso, o Material Design 3 do Flet gera todas as nuances da cor primária automaticamente.
    return tema