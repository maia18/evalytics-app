import flet as ft
from components.landing.palette import (
    FUNDO,
    CARD_ESCURO,
    BORDA_ESCURO,
    TEXTO_CLARO,
    TEXTO_CLARO_SECUNDARIO,
    ROXO,
    ROXO_CLARO,
)
from components.landing.helpers import criar_etapa

def criar_secao_sobre() -> ft.Container:
    """
    Constrói a seção 'Como funciona' da Landing Page.
        Apresenta o fluxo de avaliação em 3 etapas numeradas
        e um card destaque institucional.
    """

    # =========================================================
    # ETAPAS NUMERADAS
    # =========================================================

    bloco_etapas = ft.Column(
        spacing=16,
        controls=[

            ft.Text(
                "Como funciona",
                size=24,
                weight=ft.FontWeight.BOLD,
                color=TEXTO_CLARO,
            ),

            ft.Text(
                "Um fluxo simples em 3 passos.",
                size=13,
                color=TEXTO_CLARO_SECUNDARIO,
            ),

            ft.Container(height=4),

            criar_etapa(
                "1",
                "Avaliar",
                "Colete informações por meio das "
                "avaliações institucionais.",
                1.0,
            ),

            criar_etapa(
                "2",
                "Analisar",
                "Organize os resultados e acompanhe "
                "os indicadores.",
                0.80,
            ),

            criar_etapa(
                "3",
                "Melhorar",
                "Use as informações para apoiar "
                "decisões e melhorias.",
                0.60,
            ),
        ],
    )

    # =========================================================
    # CARD DESTAQUE
    # =========================================================

    card_destaque = ft.Container(
        padding=24,
        border_radius=16,
        bgcolor=CARD_ESCURO,
        border=ft.Border.all(
            1,
            BORDA_ESCURO,
        ),
        content=ft.Column(
            spacing=12,
            controls=[

                ft.Row(
                    spacing=8,
                    controls=[
                        ft.Container(
                            width=8,
                            height=8,
                            bgcolor=ROXO,
                            border_radius=8,
                        ),
                        ft.Text(
                            "Da avaliação à melhoria contínua",
                            size=13,
                            weight=ft.FontWeight.BOLD,
                            color=ROXO_CLARO,
                        ),
                    ],
                ),

                ft.Text(
                    "O Evalytics centraliza todo o processo de "
                    "avaliação institucional, facilitando a coleta, "
                    "organização e análise das informações de forma "
                    "estruturada.",
                    size=13,
                    color=TEXTO_CLARO_SECUNDARIO,
                ),
            ],
        ),
    )

    # =========================================================
    # SEÇÃO
    # =========================================================

    return ft.Container(
        key=ft.ScrollKey("sobre"),
        padding=ft.Padding.symmetric(
            horizontal=32,
            vertical=56,
        ),
        bgcolor=FUNDO,
        content=ft.ResponsiveRow(
            columns=12,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            run_spacing=30,
            controls=[

                # =====================================================
                # BLOCO ESQUERDO: ETAPAS
                # =====================================================

                ft.Container(
                    col={
                        "xs": 12,
                        "sm": 12,
                        "md": 6,
                        "lg": 6,
                        "xl": 6,
                    },
                    content=bloco_etapas,
                ),

                # =====================================================
                # BLOCO DIREITO: DESTAQUE
                # =====================================================

                ft.Container(
                    col={
                        "xs": 12,
                        "sm": 12,
                        "md": 6,
                        "lg": 6,
                        "xl": 6,
                    },
                    content=card_destaque,
                ),
            ],
        ),
    )
