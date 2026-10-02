import flet as ft
from typing import Callable
from database.services.firestore_courses import obter_cursos_db
from models.cursos.widgets.stats_cards import criar_stats_card
from models.cursos.widgets.tabela_cursos import criar_linha_curso, ContextoTabelaCursos
from components.core.constants.constants import (
    TEXTO_PRINCIPAL,
)
def atualizar_estatisticas(
    page: ft.Page,
    tabela_cursos: ft.DataTable,
    linha_stats: ft.Row,
    cores_layout: dict,
    estado_vazio: ft.Text,
) -> None:

    total_cursos = str(len(tabela_cursos.rows))

    departamentos_unicos = {
        linha.cells[2].content.value.strip()
        for linha in tabela_cursos.rows
        if (
            hasattr(linha.cells[2].content, "value")
            and linha.cells[2].content.value.strip()
        )
    }

    total_deptos = str(len(departamentos_unicos))

    cor_texto = cores_layout[TEXTO_PRINCIPAL]

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

def carregar_cursos_iniciais(contexto_tabela: ContextoTabelaCursos, tabela_cursos: ft.DataTable, atualizar_interface_callback: Callable[[], None]) -> None:
    """Faz a requisição inicial ao Firestore e popula a interface."""
    
    cursos = obter_cursos_db()
    tabela_cursos.rows.clear()

    for c in cursos:
        # O .get() possui um fallback seguro ("" ou "S/C") para evitar travamentos caso os dados estejam incompletos no banco
        linha = criar_linha_curso(
            contexto_tabela,
            c.get("id"),
            c.get("codigo", "S/C"),
            c.get("nome", ""),
            c.get("departamento", ""),
            c.get("coordenador", ""),
        )
        tabela_cursos.rows.append(linha)
        
    atualizar_interface_callback()