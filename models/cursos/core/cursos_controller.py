import flet as ft
from typing import Callable
from database.services.cursos.firestore_courses import obter_cursos_db
from models.cursos.widgets.tabela_cursos import criar_linha_curso, ContextoTabelaCursos

def carregar_cursos_iniciais(
    contexto_tabela: ContextoTabelaCursos, 
    tabela_cursos: ft.DataTable, 
    atualizar_interface_callback: Callable[[], None]
) -> None:
    """Faz a requisição inicial ao Firestore e popula a interface da tabela."""
    
    cursos = obter_cursos_db()
    tabela_cursos.rows.clear()

    for c in cursos:
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