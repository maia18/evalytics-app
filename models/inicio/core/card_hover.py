from typing import Callable
import flet as ft

from components.core.constants.constants import COR_PRIMARIA, BORDA
from components.core.theme.border_utils import criar_borda_uniforme

def obter_funcao_hover(layout, card: ft.Container, seta_indicadora: ft.Icon) -> Callable[[ft.ControlEvent], None]:
    """
    Fábrica que injeta as dependências visuais e retorna a função de evento de hover.
    """
    
    # Aplica (ou remove) o destaque visual quando o mouse entra/sai do card.
    def ao_passar_mouse(e: ft.ControlEvent) -> None:
        em_hover = e.data == "true"

        # Altera dinamicamente as propriedades de borda, sombra e visibilidade da seta indicadora baseada no status de hover.
        cor_borda = COR_PRIMARIA if em_hover else layout.cores[BORDA]
        card.border = criar_borda_uniforme(cor_borda)
        card.shadow = ft.BoxShadow(
            spread_radius=0, blur_radius=18 if em_hover else 0,
            color=ft.Colors.with_opacity(0.18, COR_PRIMARIA), 
            offset=ft.Offset(0, 6),
        )
        seta_indicadora.color = COR_PRIMARIA if em_hover else ft.Colors.TRANSPARENT

        card.update()

    return ao_passar_mouse