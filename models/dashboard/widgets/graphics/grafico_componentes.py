import flet as ft
from components.core.constants.constants import (
    ALTURA_MAX, 
    BORDA, 
    CARD,
)
from components.core.theme.border_utils import criar_borda_uniforme

def criar_coluna_grafico(
    nome: str,
    nota: float,
    cor: str,
    cor_texto_principal: str,
    altura_max: int = ALTURA_MAX,
) -> ft.Column:
    """Desenha uma barra vertical individual do gráfico."""
    altura_barra = (nota / 5.0) * altura_max
    
    return ft.Column(
        alignment=ft.MainAxisAlignment.END,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=6,
        controls=[
            ft.Text(f"{nota:.1f}", size=12, weight="bold", color=ft.Colors.GREY),
            ft.Container(
                width=40,
                height=altura_barra,
                bgcolor=cor,
                border_radius=4,
                tooltip=f"{nome}: {nota:.1f} / 5.0",
            ),
            ft.Text(
                nome,
                size=12,
                weight="w500",
                color=cor_texto_principal,
                text_align=ft.TextAlign.CENTER,
            ),
        ],
    )

def criar_estado_vazio(cores_layout: dict) -> ft.Container:
    """Retorna o estado visual de quando não há dados para o gráfico."""
    
    return ft.Container(
        bgcolor=cores_layout[CARD],
        padding=20,
        border_radius=8,
        border=criar_borda_uniforme(cores_layout[BORDA]),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
            controls=[
                ft.Icon(ft.Icons.BAR_CHART_OUTLINED, size=42, color=ft.Colors.GREY_400),
                ft.Text("Nenhuma avaliação registrada ainda.", color=ft.Colors.GREY_500),
            ],
        ),
    )