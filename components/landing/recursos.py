import flet as ft

from components.core.constants.constants import (
    COR_TEXTO_TITULO,
    COR_TEXTO_SECUNDARIO,
    COR_CARD,
)

from components.landing.helpers import criar_card_recurso


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
            _card(
                ft.Icons.RATE_REVIEW_OUTLINED,
                "Avaliações",
                "Colete e organize avaliações institucionais "
                "de forma estruturada.",
            ),

            _card(
                ft.Icons.INSERT_CHART_OUTLINED,
                "Indicadores",
                "Acompanhe indicadores para compreender "
                "os resultados das avaliações.",
            ),

            _card(
                ft.Icons.SCHOOL_OUTLINED,
                "Cursos",
                "Organize informações relacionadas aos "
                "cursos e à realidade acadêmica.",
            ),

            _card(
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


def _card(
    icone,
    titulo: str,
    descricao: str,
) -> ft.Container:

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