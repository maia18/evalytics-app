from typing import Callable
import flet as ft

from components.core.constants.constants import CARD, BORDA, TEXTO_PRINCIPAL, COR_PRIMARIA, COR_TEXTO_SECUNDARIO
from components.core.theme.border_utils import criar_borda_uniforme

def criar_card(
    layout, titulo: str, descricao: str, icone: str, rota: str, mudar_tela: Callable[[str], None],
) -> ft.Container:
    """Gera um cartão interativo padronizado para uso como atalho de navegação."""
    
    # Define a seta que aparecerá apenas quando houver hover (passar o mouse).
    seta_indicadora = ft.Icon(
        ft.Icons.ARROW_FORWARD_ROUNDED, color=ft.Colors.TRANSPARENT, size=18, animate_opacity=200,
    )

    # Container estilizado para o ícone do card.
    badge_icone = ft.Container(
        width=44, height=44, border_radius=10, bgcolor=ft.Colors.with_opacity(0.12, COR_PRIMARIA),
        alignment=ft.alignment.Alignment.CENTER, content=ft.Icon(icone, color=COR_PRIMARIA, size=22),
    )

    card = ft.Container(
        width=300, bgcolor=layout.cores[CARD], padding=20, border_radius=14,
        border=criar_borda_uniforme(layout.cores[BORDA]),
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=0, color=ft.Colors.with_opacity(0.18, COR_PRIMARIA), offset=ft.Offset(0, 6)),
        animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT), ink=True,
        on_click=lambda e: mudar_tela(rota),
        content=ft.Column(
            spacing=12,
            controls=[
                ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER, controls=[badge_icone, seta_indicadora]),
                ft.Text(titulo, weight="bold", size=16, color=layout.cores[TEXTO_PRINCIPAL]),
                ft.Text(descricao, size=12, color=COR_TEXTO_SECUNDARIO),
            ],
        ),
    )

    def ao_passar_mouse(e: ft.ControlEvent) -> None:
        """Aplica (ou remove) o destaque visual quando o mouse entra/sai do card."""
        em_hover = e.data == "true"

        # Altera dinamicamente as propriedades de borda, sombra e visibilidade da seta indicadora baseada no status de hover.
        cor_borda = COR_PRIMARIA if em_hover else layout.cores[BORDA]
        card.border = criar_borda_uniforme(cor_borda)
        card.shadow = ft.BoxShadow(
            spread_radius=0, blur_radius=18 if em_hover else 0,
            color=ft.Colors.with_opacity(0.18, COR_PRIMARIA), offset=ft.Offset(0, 6),
        )
        seta_indicadora.color = COR_PRIMARIA if em_hover else ft.Colors.TRANSPARENT

        card.update()

    card.on_hover = ao_passar_mouse
    return card