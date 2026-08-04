import flet as ft
from components.core.constants.constants import CARD, TEXTO_PRINCIPAL

# Linhas mockadas; preparadas para integração futura via backend.
LINHAS_EXEMPLO_RESULTADOS: list[dict] = [
    {"semestre": "2025.2", "infra": "4.8", "didatica": "4.5", "atendimento": "4.0", "material": "4.2", "inovacao": "4.7"},
    {"semestre": "2026.1", "infra": "Aguardando", "didatica": "-", "atendimento": "-", "material": "-", "inovacao": "-"},
]

def _criar_linha_resultado(item: dict) -> ft.DataRow:
    """Constrói uma linha da tabela a partir de um dicionário iterado."""
    return ft.DataRow(cells=[
        ft.DataCell(ft.Text(item["semestre"], color=ft.Colors.ON_SURFACE)),
        ft.DataCell(ft.Text(item["infra"], color=ft.Colors.ON_SURFACE)),
        ft.DataCell(ft.Text(item["didatica"], color=ft.Colors.ON_SURFACE)),
        ft.DataCell(ft.Text(item["atendimento"], color=ft.Colors.ON_SURFACE)),
        ft.DataCell(ft.Text(item["material"], color=ft.Colors.ON_SURFACE)),
        ft.DataCell(ft.Text(item["inovacao"], color=ft.Colors.ON_SURFACE)),
    ])

def criar_tabela_resultados(page: ft.Page, layout, borda_container: ft.Border) -> ft.Container:
    """Tabela nativa com o consolidado das avaliações institucionais por eixo e semestre."""
    return ft.Container(
        expand=True, bgcolor=layout.cores[CARD], padding=25, border=borda_container, border_radius=10,
        content=ft.Column(controls=[
            ft.Text("Resultados Consolidados", size=18, weight="bold", color=layout.cores[TEXTO_PRINCIPAL]),
            ft.DataTable(
                # Ajusta a cor do cabeçalho caso o tema mude.
                heading_row_color=ft.Colors.BLUE_GREY_900 if page.theme_mode == ft.ThemeMode.DARK else ft.Colors.BLUE_50,
                columns=[
                    ft.DataColumn(ft.Text("Semestre", weight="bold", color=ft.Colors.ON_SURFACE)),
                    ft.DataColumn(ft.Text("Infraestrutura", weight="bold", color=ft.Colors.ON_SURFACE)),
                    ft.DataColumn(ft.Text("Didática", weight="bold", color=ft.Colors.ON_SURFACE)),
                    ft.DataColumn(ft.Text("Atendimento", weight="bold", color=ft.Colors.ON_SURFACE)),
                    ft.DataColumn(ft.Text("Material", weight="bold", color=ft.Colors.ON_SURFACE)),
                    ft.DataColumn(ft.Text("Inovação", weight="bold", color=ft.Colors.ON_SURFACE)),
                ],
                rows=[_criar_linha_resultado(item) for item in LINHAS_EXEMPLO_RESULTADOS],
            ),
        ]),
    )