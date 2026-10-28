import flet as ft

from models.cursos.widgets.stats_cards import criar_stats_card
from database.services.cursos.firestore_courses import curso_esta_ativo


def atualizar_estatisticas(
    page: ft.Page,
    linha_stats: ft.Row,
    cores_layout: dict,
    cursos: list[dict],
) -> None:
    """Atualiza os indicadores com base no catálogo completo de cursos."""
    total_cursos = len(cursos)
    cursos_ativos = sum(1 for curso in cursos if curso_esta_ativo(curso))
    departamentos = {
        str(curso.get("departamento", "")).strip().casefold()
        for curso in cursos
        if str(curso.get("departamento", "")).strip()
    }

    linha_stats.controls = [
        criar_stats_card("Total de Cursos", str(total_cursos), cores_layout),
        criar_stats_card("Cursos Ativos", str(cursos_ativos), cores_layout),
        criar_stats_card("Departamentos", str(len(departamentos)), cores_layout),
    ]
    page.update()
