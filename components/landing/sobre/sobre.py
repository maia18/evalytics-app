import flet as ft
from components.core.constants.constants import (
    COR_CARD,
)
from components.landing.helpers import criar_etapa
from components.landing.sobre.conteudo import criar_sobre_conteudo

def criar_secao_sobre() -> ft.Container:

    sobre_conteudo = criar_sobre_conteudo()
    etapas = ft.Column(
        spacing=22,
        controls=[
            criar_etapa(
                "01",
                "Avaliar",
                "Colete informações por meio das avaliações institucionais.",
            ),
            criar_etapa(
                "02",
                "Analisar",
                "Organize os resultados e acompanhe os indicadores.",
            ),
            criar_etapa(
                "03",
                "Melhorar",
                "Use as informações para apoiar decisões e melhorias.",
            ),
        ],
    )

    return ft.Container(
        key=ft.ScrollKey("sobre"),
        padding=ft.Padding.symmetric(
            horizontal=60,
            vertical=75,
        ),
        bgcolor=COR_CARD,
        content=ft.ResponsiveRow(
            columns=12,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            run_spacing=35,
            controls=[
                
                # =====================================================
                # TEXTO
                # =====================================================

                ft.Container(
                    col={
                        "xs": 12,
                        "sm": 12,
                        "md": 6,
                        "lg": 6,
                        "xl": 6,
                    },
                    padding=ft.Padding.only(
                        right=40,
                    ),
                    content=sobre_conteudo,
                ),

                # =====================================================
                # ETAPAS
                # =====================================================

                ft.Container(
                    col={
                        "xs": 12,
                        "sm": 12,
                        "md": 6,
                        "lg": 6,
                        "xl": 6,
                    },
                    padding=ft.Padding.only(
                        top=10,
                    ),
                    content=etapas,
                ),
            ],
        ),
    )