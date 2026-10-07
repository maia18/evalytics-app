import flet as ft

from components.landing.helpers.recursos import criar_card_recurso


def criar_card_responsivo(
    icone,
    titulo: str,
    descricao: str,
) -> ft.Container:
    """
    Wrapper responsivo para os cards de recursos.
    """

    return ft.Container(
        col={
            "xs": 12,
            "sm": 12,
            "md": 6,
            "lg": 3,
            "xl": 3,
        },
        alignment=ft.Alignment.CENTER,
        content=criar_card_recurso(
            icone,
            titulo,
            descricao,
        ),
    )