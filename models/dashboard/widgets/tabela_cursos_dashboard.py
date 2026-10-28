import flet as ft

from components.core.constants.constants import (
    CARD,
    CARD_SECUNDARIO,
    BORDA,
    TEXTO_PRINCIPAL,
    TEXTO_SECUNDARIO,
)
from components.core.theme.border_utils import criar_borda_uniforme


def criar_tabela_cursos_dashboard(layout, dados_por_curso: list[dict]) -> ft.Container:
    """Resume avaliações, respostas e média para cada curso selecionado."""
    if not dados_por_curso:
        tabela = ft.Text(
            "Nenhum curso possui dados para os filtros selecionados.",
            color=layout.cores[TEXTO_SECUNDARIO],
        )
    else:
        tabela = ft.DataTable(
            expand=True,
            column_spacing=8,
            heading_row_color=layout.cores[CARD_SECUNDARIO],
            columns=[
                ft.DataColumn(ft.Text("Curso", size=10, weight="bold")),
                ft.DataColumn(ft.Text("Avaliações", size=10, weight="bold"), numeric=True),
                ft.DataColumn(ft.Text("Respostas", size=10, weight="bold"), numeric=True),
                ft.DataColumn(ft.Text("Média (1–5)", size=10, weight="bold"), numeric=True),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Text(
                                item["curso"],
                                size=10,
                                max_lines=2,
                                color=layout.cores[TEXTO_PRINCIPAL],
                            )
                        ),
                        ft.DataCell(ft.Text(str(item["avaliacoes"]), size=10)),
                        ft.DataCell(ft.Text(str(item["respostas"]), size=10)),
                        ft.DataCell(
                            ft.Text(
                                f"{item['media_geral']:.1f}"
                                if item["media_geral"] is not None
                                else "—",
                                weight="bold",
                                size=10,
                            )
                        ),
                    ]
                )
                for item in dados_por_curso
            ],
        )

    return ft.Container(
        bgcolor=layout.cores[CARD],
        padding=8,
        border_radius=8,
        border=criar_borda_uniforme(layout.cores[BORDA]),
        content=ft.Column(
            spacing=12,
            controls=[
                ft.Column(
                    spacing=4,
                    controls=[
                        ft.Text(
                            "Visão geral por curso",
                            size=15,
                            weight="bold",
                            color=layout.cores[TEXTO_PRINCIPAL],
                        ),
                        ft.Text(
                            "Avaliações realizadas, respostas registradas e média das respostas válidas.",
                            size=10,
                            color=layout.cores[TEXTO_SECUNDARIO],
                        ),
                    ],
                ),
                ft.Row(
                    scroll=ft.ScrollMode.AUTO,
                    controls=[tabela],
                ),
            ],
        ),
    )
