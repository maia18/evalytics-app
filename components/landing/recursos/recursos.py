import flet as ft

from components.core.constants.constants import (
    COR_TEXTO_TITULO,
    COR_TEXTO_SECUNDARIO,
    COR_CARD,
)

from components.landing.recursos.card import criar_card_responsivo


def criar_secao_recursos() -> ft.Container:
    """
    Constrói a seção de recursos da Landing Page.

    Apresenta os principais módulos do Evalytics
    em uma grade responsiva.
    """

    # =========================================================
    # CABEÇALHO DA SEÇÃO
    # =========================================================

    titulo_recursos = ft.Column(
        width=720,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
        controls=[
            ft.Text(
                "Uma plataforma para melhoria contínua",
                size=30,
                weight=ft.FontWeight.BOLD,
                color=COR_TEXTO_TITULO,
                text_align=ft.TextAlign.CENTER,
            ),

            ft.Text(
                "Organize avaliações, acompanhe indicadores e "
                "transforme informações acadêmicas em apoio "
                "para a gestão institucional.",
                size=15,
                color=COR_TEXTO_SECUNDARIO,
                text_align=ft.TextAlign.CENTER,
            ),
        ],
    )

    # =========================================================
    # CARDS DE RECURSOS
    # =========================================================

    cards_recursos = ft.ResponsiveRow(
        columns=12,
        alignment=ft.MainAxisAlignment.CENTER,
        run_spacing=20,
        spacing=10,
        controls=[
            criar_card_responsivo(
                ft.Icons.RATE_REVIEW_OUTLINED,
                "Avaliações",
                "Colete e organize avaliações institucionais de forma estruturada.",
            ),

            criar_card_responsivo(
                ft.Icons.INSERT_CHART_OUTLINED,
                "Indicadores",
                "Acompanhe indicadores para compreender os resultados das avaliações.",
            ),

            criar_card_responsivo(
                ft.Icons.SCHOOL_OUTLINED,
                "Cursos",
                "Organize informações relacionadas aos cursos e à realidade acadêmica.",
            ),

            criar_card_responsivo(
                ft.Icons.ASSESSMENT_OUTLINED,
                "Relatórios",
                "Visualize resultados de forma organizada para apoiar a análise institucional.",
            ),
        ],
    )

    # =========================================================
    # SEÇÃO
    # =========================================================

    return ft.Container(
        key=ft.ScrollKey("recursos"),
        padding=ft.Padding.symmetric(
            horizontal=40,
            vertical=72,
        ),
        bgcolor=COR_CARD,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=42,
            controls=[
                titulo_recursos,
                cards_recursos,
            ],
        ),
    )