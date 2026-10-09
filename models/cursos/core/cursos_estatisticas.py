import flet as ft
from models.cursos.widgets.stats_cards import criar_stats_card
from components.core.constants.constants import TEXTO_PRINCIPAL

def extrair_total_departamentos(linhas_tabela: list[ft.DataRow]) -> int:
    """Extrai a quantidade de departamentos únicos iterando pelas células da tabela."""
    
    departamentos_unicos = {
        linha.cells[2].content.value.strip()
        for linha in linhas_tabela
        if hasattr(linha.cells[2].content, "value") and linha.cells[2].content.value.strip()
    }
    return len(departamentos_unicos)

def atualizar_estatisticas(
    page: ft.Page,
    tabela_cursos: ft.DataTable,
    linha_stats: ft.Row,
    cores_layout: dict,
    estado_vazio: ft.Text,
) -> None:
    """Atualiza os cards numéricos de estatísticas e a visibilidade da tabela de cursos."""
    
    total_cursos = str(len(tabela_cursos.rows))
    total_deptos = str(extrair_total_departamentos(tabela_cursos.rows))

    linha_stats.controls = [
        criar_stats_card(
            "Total de Cursos",
            total_cursos,
            cores_layout,
        ),
        criar_stats_card(
            "Cursos Ativos",
            "0",
            cores_layout,
        ),
        criar_stats_card(
            "Departamentos",
            total_deptos,
            cores_layout,
        ),
    ]

    estado_vazio.visible = len(tabela_cursos.rows) == 0
    tabela_cursos.visible = len(tabela_cursos.rows) > 0

    page.update()