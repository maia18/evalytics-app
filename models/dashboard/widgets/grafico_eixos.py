import flet as ft

from components.core.constants.constants import (
    ALTURA_MAX,
    BORDA,
    CARD,
    TEXTO_PRINCIPAL,
)
from components.core.theme.border_utils import criar_borda_uniforme


ALTURA_AREA_PLOTAGEM = 200


def criar_coluna_grafico(
    layout,
    nome: str,
    nota: float,
    cor: str,
    altura_max: int = ALTURA_MAX,
) -> ft.Column:
    """
    Desenha uma barra vertical individual do gráfico.
    """

    altura_barra = (nota / 5.0) * altura_max

    return ft.Column(
        alignment=ft.MainAxisAlignment.END,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=6,
        controls=[
            ft.Text(
                f"{nota:.1f}",
                size=12,
                weight="bold",
                color=ft.Colors.GREY,
            ),
            ft.Container(
                width=40,
                height=altura_barra,
                bgcolor=cor,
                border_radius=4,
                tooltip=f"{nome}: {nota:.1f} / 5.0",
            ),
            ft.Text(
                nome,
                size=12,
                weight="w500",
                color=layout.cores[TEXTO_PRINCIPAL],
                text_align=ft.TextAlign.CENTER,
            ),
        ],
    )


def criar_grafico_eixos(
    layout,
    medias_eixos: dict[int, float],
    nomes_eixos: dict[int, str],
    cores_barras: list[str],
) -> ft.Container:
    """
    Constrói o gráfico de desempenho médio por eixo.
    """

    barras_grafico = []

    for i, (eixo_id, nota) in enumerate(
        sorted(medias_eixos.items())
    ):
        nome = nomes_eixos.get(
            eixo_id,
            f"Eixo {eixo_id}",
        )

        cor = cores_barras[
            i % len(cores_barras)
        ]

        barras_grafico.append(
            criar_coluna_grafico(
                layout,
                nome,
                nota,
                cor,
            )
        )

    # ==========================================================
    # ESTADO VAZIO
    # ==========================================================

    if not barras_grafico:
        return ft.Container(
            bgcolor=layout.cores[CARD],
            padding=20,
            border_radius=8,
            border=criar_borda_uniforme(
                layout.cores[BORDA]
            ),
            content=ft.Column(
                horizontal_alignment=(
                    ft.CrossAxisAlignment.CENTER
                ),
                spacing=8,
                controls=[
                    ft.Icon(
                        ft.Icons.BAR_CHART_OUTLINED,
                        size=42,
                        color=ft.Colors.GREY_400,
                    ),
                    ft.Text(
                        "Nenhuma avaliação registrada ainda.",
                        color=ft.Colors.GREY_500,
                    ),
                ],
            ),
        )

    # ==========================================================
    # GRÁFICO
    # ==========================================================

    return ft.Container(
        bgcolor=layout.cores[CARD],
        padding=20,
        border_radius=8,
        border=criar_borda_uniforme(
            layout.cores[BORDA]
        ),
        content=ft.Column(
            spacing=14,
            controls=[
                ft.Column(
                    spacing=4,
                    controls=[
                        ft.Text(
                            "Desempenho médio por eixo",
                            size=18,
                            weight="bold",
                            color=layout.cores[
                                TEXTO_PRINCIPAL
                            ],
                        ),
                        ft.Text(
                            "Média das respostas registradas "
                            "nas avaliações institucionais.",
                            size=14,
                            color=ft.Colors.GREY,
                        ),
                    ],
                ),
                ft.Container(
                    height=ALTURA_AREA_PLOTAGEM,
                    padding=ft.Padding.only(
                        left=12,
                        right=12,
                        top=8,
                        bottom=4,
                    ),
                    content=ft.Row(
                        alignment=(
                            ft.MainAxisAlignment.SPACE_AROUND
                        ),
                        vertical_alignment=(
                            ft.CrossAxisAlignment.END
                        ),
                        controls=barras_grafico,
                    ),
                ),
            ],
        ),
    )