import flet as ft
from typing import Callable

from database.services.cursos.firestore_courses import (
    curso_esta_ativo,
    obter_cursos_db,
)
from models.cursos.widgets.tabela_cursos import (
    ContextoTabelaCursos,
    criar_linha_curso,
)
from utils.services.avaliacoes.avaliacoes_service import listar_avaliacoes
from utils.services.cursos.curso_utils import (
    chave_curso,
    nome_departamento_exibicao,
    normalizar_nome_curso,
)


def carregar_cursos_iniciais(
    contexto_tabela: ContextoTabelaCursos,
    tabela_cursos: ft.DataTable,
    atualizar_interface_callback: Callable[[], None],
) -> None:
    """Carrega cursos e avaliações, depois reconstrói as linhas da tabela."""
    cursos = obter_cursos_db()
    avaliacoes = listar_avaliacoes()
    nomes_cadastrados = [
        str(curso.get("nome", "")).strip()
        for curso in cursos
        if curso.get("nome") and str(curso.get("nome")).strip()
    ]
    contagem_por_nome: dict[str, int] = {}

    for avaliacao in avaliacoes:
        curso_nome = normalizar_nome_curso(
            avaliacao.get("curso_nome", avaliacao.get("curso", "")),
            nomes_cadastrados,
        )
        chave = chave_curso(curso_nome)
        if chave:
            contagem_por_nome[chave] = contagem_por_nome.get(chave, 0) + 1

    linhas = []
    for curso in cursos:
        nome = curso.get("nome", "")
        quantidade_avaliacoes = contagem_por_nome.get(
            chave_curso(normalizar_nome_curso(nome, nomes_cadastrados)), 0
        )
        linhas.append(
            criar_linha_curso(
                contexto_tabela,
                curso.get("id"),
                curso.get("codigo", ""),
                nome,
                nome_departamento_exibicao(
                    curso.get("departamento", ""), cursos
                ),
                curso.get("coordenador", ""),
                curso_esta_ativo(curso),
                quantidade_avaliacoes,
            )
        )

    contexto_tabela.estado["cursos"] = cursos
    contexto_tabela.estado["todas_linhas"] = linhas
    tabela_cursos.rows = linhas
    atualizar_interface_callback()
