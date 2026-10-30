import flet as ft
from components.landing.palette import FUNDO, SUPERFICIE, TEXTO, TEXTO_SECUNDARIO, ROXO, ROSA, CIANO, LARANJA
from components.landing.recursos.card import criar_card_responsivo

def criar_secao_recursos() -> ft.Container:
    """
    Constrói a seção de recursos da Landing Page.
        Apresenta os principais módulos do Evalytics em uma grade 2×2 com layout horizontal.
    """

    # =========================================================
    # CABEÇALHO DA SEÇÃO
    # =========================================================

    titulo_recursos = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
        controls=[
            ft.Text(
                "Tudo em um só lugar",
                size=28,
                weight=ft.FontWeight.BOLD,
                color=TEXTO,
                text_align=ft.TextAlign.CENTER,
            ),

            ft.Container(
                width=float("inf"),
                content=ft.Text(
                    "Módulos integrados para cobrir todo o ciclo "
                    "de avaliação institucional.",
                    size=14,
                    color=TEXTO_SECUNDARIO,
                    text_align=ft.TextAlign.CENTER,
                ),
            ),
        ],
    )

    # =========================================================
    # CARDS DE RECURSOS
    # =========================================================

    cards_recursos = ft.ResponsiveRow(
        columns=12,
        alignment=ft.MainAxisAlignment.CENTER,
        run_spacing=16,
        spacing=16,
        controls=[
            criar_card_responsivo(
                ft.Icons.RATE_REVIEW_OUTLINED,
                "Avaliações",
                "Colete e organize avaliações institucionais "
                "de forma estruturada e eficiente.",
                ROXO,
            ),

            criar_card_responsivo(
                ft.Icons.INSERT_CHART_OUTLINED,
                "Indicadores",
                "Acompanhe indicadores que ajudam a compreender "
                "os resultados das avaliações.",
                CIANO,
            ),

            criar_card_responsivo(
                ft.Icons.SCHOOL_OUTLINED,
                "Cursos",
                "Organize informações relacionadas aos cursos "
                "e à realidade acadêmica.",
                ROSA,
            ),

            criar_card_responsivo(
                ft.Icons.ASSESSMENT_OUTLINED,
                "Relatórios",
                "Visualize resultados de forma organizada para "
                "apoiar a análise institucional.",
                LARANJA,
            ),
        ],
    )

    # =========================================================
    # SEÇÃO
    # =========================================================

    return ft.Container(
        key=ft.ScrollKey("recursos"),
        padding=ft.Padding.symmetric(
            horizontal=32,
            vertical=56,
        ),
        bgcolor=FUNDO,
        gradient=ft.LinearGradient(
            begin=ft.Alignment.TOP_CENTER,
            end=ft.Alignment.BOTTOM_CENTER,
            colors=[FUNDO, "#BBA5D7", SUPERFICIE, SUPERFICIE, "#BBA5D7", FUNDO],
            stops=[0, 0.12, 0.24, 0.76, 0.88, 1],
        ),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=36,
            controls=[
                titulo_recursos,
                cards_recursos,
            ],
        ),
    )
