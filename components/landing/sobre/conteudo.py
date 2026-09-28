import flet as ft

from components.core.constants.constants import (
    COR_TEXTO_TITULO,
    COR_TEXTO_SECUNDARIO,
    COR_PRIMARIA,
)


def criar_sobre_conteudo() -> ft.Column:

    return ft.Column(
        spacing=16,
        controls=[
            ft.Text(
                "Sobre o Evalytics",
                size=28,
                weight=ft.FontWeight.BOLD,
                color=COR_TEXTO_TITULO,
            ),

            ft.Text(
                "O Evalytics foi pensado para centralizar o processo "
                "de avaliação institucional em uma única plataforma.",
                size=16,
                color=COR_TEXTO_SECUNDARIO,
            ),

            ft.Text(
                "A proposta é facilitar a coleta, organização e "
                "análise das informações produzidas pelas avaliações, "
                "permitindo que esses dados sejam acompanhados de "
                "forma mais estruturada.",
                size=15,
                color=COR_TEXTO_SECUNDARIO,
            ),

            ft.Text(
                "Da avaliação à melhoria contínua.",
                size=16,
                weight=ft.FontWeight.BOLD,
                color=COR_PRIMARIA,
            ),
        ],
    )