from typing import Callable
import flet as ft

from components.core.constants.constants import CARD
from models.relatorios.core.export_pdf import gerar_pdf_completo
from models.avaliacoes.core.export_csv import exportar_csv

# Dados de exemplo (Mock). Podem ser substituídos por consultas ao Firestore futuramente.
MEDIAS_MOCK: dict[int, float] = {1: 4.8, 2: 4.5, 3: 4.7}
NOMES_EIXOS_MOCK: dict[int, str] = {1: "Infraestrutura", 2: "Didática", 3: "Atendimento"}

def criar_secao_filtros(layout, borda_container: ft.Border, page: ft.Page) -> ft.Container:
    """Barra superior de filtros (Dropdowns) e ações de exportação (CSV/PDF)."""
    
    dropdown_semestre = ft.Dropdown(
        label="Semestre", options=[ft.dropdown.Option("2026.1"), ft.dropdown.Option("2025.2")], value="2026.1", width=200, dense=True,
    )

    dropdown_eixo = ft.Dropdown(
        label="Eixo Avaliativo", options=[ft.dropdown.Option("Infraestrutura"), ft.dropdown.Option("Didática"), ft.dropdown.Option("Atendimento")],
        width=200, dense=True,
    )

    return ft.Container(
        bgcolor=layout.cores[CARD], padding=20, border_radius=8, border=borda_container,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row([dropdown_semestre, dropdown_eixo], spacing=10),
                ft.Row(spacing=10, controls=[
                    ft.ElevatedButton("Exportar CSV", icon=ft.Icons.TABLE_VIEW, bgcolor=ft.Colors.GREEN_700, color=ft.Colors.WHITE, on_click=lambda e: exportar_csv(page)),
                    ft.ElevatedButton("Gerar Documento (PDF)", icon=ft.Icons.PICTURE_AS_PDF, bgcolor=ft.Colors.RED_700, color=ft.Colors.WHITE, on_click=lambda e: gerar_pdf_completo(page, medias=MEDIAS_MOCK, nomes_eixos=NOMES_EIXOS_MOCK, semestre=dropdown_semestre.value)),
                ]),
            ],
        ),
    )