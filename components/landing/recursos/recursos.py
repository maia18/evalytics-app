import flet as ft

from components.core.constants.constants import (
    COR_TEXTO_TITULO,
    COR_TEXTO_SECUNDARIO,
    COR_CARD,
)

from components.landing.recursos.card import criar_card_responsivo


def criar_secao_recursos() -> ft.Container:

    titulo_recursos = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=8,
        controls=[
            ft.Text(
                "Uma plataforma para melhoria contínua",
                size=28,
                weight=ft.FontWeight.BOLD,
                color=COR_TEXTO_TITULO,
                text_align=ft.TextAlign.CENTER,
            ),

            ft.Container(
                padding=ft.Padding.symmetric(
                    horizontal=10,
                ),
                content=ft.Text(
                    "Organize avaliações, acompanhe indicadores e "
                    "transforme informações acadêmicas em apoio "
                    "para a gestão institucional.",
                    size=15,
                    color=COR_TEXTO_SECUNDARIO,
                    text_align=ft.TextAlign.CENTER,
                ),
            ),
        ],
    )

    cards_recursos = ft.ResponsiveRow(
        columns=12,
        alignment=ft.MainAxisAlignment.CENTER,
        run_spacing=18,
        controls=[
            criar_card_responsivo(
                ft.Icons.RATE_REVIEW_OUTLINED,
                "Avaliações",
                "Colete e organize avaliações institucionais "
                "de forma estruturada.",
            ),

            criar_card_responsivo(
                ft.Icons.INSERT_CHART_OUTLINED,
                "Indicadores",
                "Acompanhe indicadores para compreender "
                "os resultados das avaliações.",
            ),

            criar_card_responsivo(
                ft.Icons.SCHOOL_OUTLINED,
                "Cursos",
                "Organize informações relacionadas aos "
                "cursos e à realidade acadêmica.",
            ),

            criar_card_responsivo(
                ft.Icons.ASSESSMENT_OUTLINED,
                "Relatórios",
                "Visualize resultados de forma organizada "
                "para apoiar a análise institucional.",
            ),
        ],
    )

    return ft.Container(
        key=ft.ScrollKey("recursos"),
        padding=ft.Padding.symmetric(
            horizontal=20,
            vertical=75,
        ),
        bgcolor=COR_CARD,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=35,
            controls=[
                titulo_recursos,
                cards_recursos,
            ],
        ),
    )