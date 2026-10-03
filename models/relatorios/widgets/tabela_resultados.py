import flet as ft

from components.core.constants.constants import (
    CARD,
    TEXTO_PRINCIPAL,
)
from utils.services.relatorio_service import (
    listar_resultados_consolidados,
)


NOMES_EIXOS = {
    1: "Organização Didático-Pedagógica",
    2: "Corpo Docente e Tutorial",
    3: "Infraestrutura",
}


def _formatar_nota(nota: float) -> str:
    """
    Formata uma nota numérica para exibição na tabela.
    """

    return f"{nota:.1f}"


def _formatar_data(data_iso: str) -> str:
    """
    Converte uma data ISO 8601 para o formato DD/MM/YYYY.
    """

    if not data_iso:
        return "-"

    try:
        data = data_iso[:10]
        ano, mes, dia = data.split("-")
        return f"{dia}/{mes}/{ano}"

    except (ValueError, AttributeError):
        return data_iso


def _criar_linha_resultado(item: dict) -> ft.DataRow:
    """
    Constrói uma linha da tabela a partir de uma avaliação consolidada.
    """

    eixos = item.get("eixos", {})

    curso_nome = item.get(
        "curso_nome",
        "Curso não informado",
    )

    data_avaliacao = _formatar_data(
        item.get("data_avaliacao", "")
    )

    eixo_1 = eixos.get(1, 0.0)
    eixo_2 = eixos.get(2, 0.0)
    eixo_3 = eixos.get(3, 0.0)

    media_geral = item.get(
        "media_geral",
        0.0,
    )

    return ft.DataRow(
        cells=[
            ft.DataCell(
                ft.Text(
                    curso_nome,
                    color=ft.Colors.ON_SURFACE,
                )
            ),
            ft.DataCell(
                ft.Text(
                    data_avaliacao,
                    color=ft.Colors.ON_SURFACE,
                )
            ),
            ft.DataCell(
                ft.Text(
                    _formatar_nota(eixo_1),
                    color=ft.Colors.ON_SURFACE,
                )
            ),
            ft.DataCell(
                ft.Text(
                    _formatar_nota(eixo_2),
                    color=ft.Colors.ON_SURFACE,
                )
            ),
            ft.DataCell(
                ft.Text(
                    _formatar_nota(eixo_3),
                    color=ft.Colors.ON_SURFACE,
                )
            ),
            ft.DataCell(
                ft.Text(
                    _formatar_nota(media_geral),
                    weight="bold",
                    color=ft.Colors.ON_SURFACE,
                )
            ),
        ]
    )


def criar_tabela_resultados(
    page: ft.Page,
    layout,
    borda_container: ft.Border,
) -> ft.Container:
    """
    Tabela com o consolidado real das avaliações institucionais.

    Os dados são carregados diretamente do Firestore através
    do relatorio_service.
    """

    resultados = listar_resultados_consolidados()

    linhas = [
        _criar_linha_resultado(item)
        for item in resultados
    ]

    # ==========================================================
    # ESTADO VAZIO
    # ==========================================================

    if not resultados:
        conteudo = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12,
            controls=[
                ft.Icon(
                    ft.Icons.INSERT_CHART_OUTLINED,
                    size=48,
                    color=ft.Colors.GREY_500,
                ),
                ft.Text(
                    "Nenhuma avaliação encontrada.",
                    size=16,
                    weight="bold",
                    color=ft.Colors.ON_SURFACE,
                ),
                ft.Text(
                    "Os resultados aparecerão aqui após "
                    "a conclusão de uma avaliação.",
                    size=13,
                    color=ft.Colors.GREY_600,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
        )

    else:
        conteudo = ft.DataTable(
            heading_row_color=(
                ft.Colors.BLUE_GREY_900
                if page.theme_mode == ft.ThemeMode.DARK
                else ft.Colors.BLUE_50
            ),
            columns=[
                ft.DataColumn(
                    ft.Text(
                        "Curso",
                        weight="bold",
                        color=ft.Colors.ON_SURFACE,
                    )
                ),
                ft.DataColumn(
                    ft.Text(
                        "Data",
                        weight="bold",
                        color=ft.Colors.ON_SURFACE,
                    )
                ),
                ft.DataColumn(
                    ft.Text(
                        "Eixo 1",
                        weight="bold",
                        color=ft.Colors.ON_SURFACE,
                    )
                ),
                ft.DataColumn(
                    ft.Text(
                        "Eixo 2",
                        weight="bold",
                        color=ft.Colors.ON_SURFACE,
                    )
                ),
                ft.DataColumn(
                    ft.Text(
                        "Eixo 3",
                        weight="bold",
                        color=ft.Colors.ON_SURFACE,
                    )
                ),
                ft.DataColumn(
                    ft.Text(
                        "Média Geral",
                        weight="bold",
                        color=ft.Colors.ON_SURFACE,
                    )
                ),
            ],
            rows=linhas,
        )

    # ==========================================================
    # CONTAINER
    # ==========================================================

    return ft.Container(
        expand=True,
        bgcolor=layout.cores[CARD],
        padding=25,
        border=borda_container,
        border_radius=10,
        content=ft.Column(
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Text(
                    "Resultados Consolidados",
                    size=18,
                    weight="bold",
                    color=layout.cores[TEXTO_PRINCIPAL],
                ),
                ft.Container(height=15),
                conteudo,
            ],
        ),
    )