from components.core.constants.constants import (
    LARGURA_BREAKPOINT_MOBILE,
    LARGURA_BREAKPOINT_DESKTOP,
)

def obter_categoria_layout(largura: float) -> str:
    """
    Classifica a largura da janela em uma categoria de layout.
        Função pura, ideal para testes unitários.
    """
    if largura < LARGURA_BREAKPOINT_MOBILE:
        return "mobile"
    if largura < LARGURA_BREAKPOINT_DESKTOP:
        return "compacta"
    return "desktop"