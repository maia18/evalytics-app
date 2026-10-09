import flet as ft
from components.core.constants.constants import (
    BORDA, 
    CARD, 
    TEXTO_PRINCIPAL,
)
from components.core.theme.border_utils import criar_borda_uniforme
from .grafico_componentes import criar_coluna_grafico, criar_estado_vazio

def criar_grafico_eixos(
    layout,
    medias_eixos: dict[int, float],
    nomes_eixos: dict[int, str],
    cores_barras: list[str],
) -> ft.Container:
    """Constrói o gráfico de desempenho médio por eixo."""

    barras_grafico = []
    cor_texto = layout.cores[TEXTO_PRINCIPAL]

    # Mapeamento dos dados para o componente visual
    for i, (eixo_id, nota) in enumerate(sorted(medias_eixos.items())):
        nome = nomes_eixos.get(eixo_id, f"Eixo {eixo_id}")
        cor = cores_barras[i % len(cores_barras)]

        barras_grafico.append(
            criar_coluna_grafico(nome, nota, cor, cor_texto)
        )

    # Tratamento imediato de estado vazio delegando a criação da UI
    if not barras_grafico:
        return criar_estado_vazio(layout.cores)

    # Montagem do layout final do gráfico
    return ft.Container(
        bgcolor=layout.cores[CARD],
        padding=20,
        border_radius=8,
        border=criar_borda_uniforme(layout.cores[BORDA]),
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
                            color=cor_texto,
                        ),
                        ft.Text(
                            "Média das respostas registradas nas avaliações institucionais.",
                            size=14,
                            color=ft.Colors.GREY,
                        ),
                    ],
                ),
                ft.Container(
                    height=200,
                    padding=ft.Padding.only(left=12, right=12, top=8, bottom=4),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                        vertical_alignment=ft.CrossAxisAlignment.END,
                        controls=barras_grafico,
                    ),
                ),
            ],
        ),
    )