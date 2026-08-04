import flet as ft

from components.core.constants.constants import BORDA, CARD, TEXTO_PRINCIPAL
from components.core.theme.border_utils import criar_borda_uniforme


def criar_kpi_card(layout, titulo: str, valor: str, icone: str, cor_icone: str) -> ft.Container:
    """Constrói um cartão de KPI contendo título, valor em destaque e um ícone representativo."""
    return ft.Container(
        width=240,  # Trava a largura para os cartões ficarem uniformes
        bgcolor=layout.cores[CARD],
        padding=16,
        border_radius=8,
        border=criar_borda_uniforme(layout.cores[BORDA]),
        content=ft.Column(
            spacing=10,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(titulo, size=14, color=ft.Colors.GREY_600, weight="w500"),
                        ft.Icon(icone, color=cor_icone, size=18),
                    ],
                ),
                ft.Text(valor, size=28, weight="bold", color=layout.cores[TEXTO_PRINCIPAL]),
            ],
        ),
    )