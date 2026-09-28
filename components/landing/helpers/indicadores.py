import flet as ft

from components.core.constants.constants import (
    COR_TEXTO_SECUNDARIO,
    COR_PRIMARIA,
)

def criar_indicador(
    titulo: str,
    valor: str,
) -> ft.Container:
    """Cria um card de indicador utilizado para destacar métricas, números ou informações relevantes."""

    return ft.Container(
        expand=True,
        padding=15,
        bgcolor=ft.Colors.with_opacity(
            0.06,
            COR_PRIMARIA,
        ),
        border_radius=10,
        content=ft.Column(
            spacing=5,
            controls=[
                ft.Text(
                    titulo,
                    size=12,
                    color=COR_TEXTO_SECUNDARIO,
                ),

                ft.Text(
                    valor,
                    size=26,
                    weight=ft.FontWeight.BOLD,
                    color=COR_PRIMARIA,
                ),
            ],
        ),
    )