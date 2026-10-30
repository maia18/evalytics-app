import flet as ft
from components.landing.helpers.recursos import criar_card_recurso

def criar_card_responsivo(
    icone,
    titulo: str,
    descricao: str,
    cor_acento: str,
) -> ft.Container:
    """Wrapper responsivo para os cards de recursos em grid 2×2."""

    return ft.Container(
        col={
            "xs": 12,
            "sm": 12,
            "md": 6,
            "lg": 6,
            "xl": 6,
        },
        alignment=ft.Alignment.CENTER,
        content=criar_card_recurso(
            icone,
            titulo,
            descricao,
            cor_acento,
        ),
    )
