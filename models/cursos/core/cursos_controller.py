import flet as ft
from typing import Callable
from database.services.cursos.firestore_courses import obter_cursos_db
from models.cursos.widgets.tabela_cursos import (
    criar_linha_curso, 
    ContextoTabelaCursos,
)

def carregar_cursos_iniciais(
    contexto_tabela: ContextoTabelaCursos, 
    tabela_cursos: ft.DataTable, 
    atualizar_interface_callback: Callable[[], None]
) -> None:
    """
    Busca os dados dos cursos no Firestore e renderiza as linhas no componente DataTable.
        Esta função atua como uma ponte (Controller) entre o Banco de Dados e a View (Tabela).
    
    Args:
        contexto_tabela: Objeto de estado contendo referências para modais/edições dos cursos.
        tabela_cursos: A instância física do componente DataTable na interface do Flet.
        atualizar_interface_callback: Função (geralmente `page.update()`) para repintar a tela.
    """
    
    # 1. Busca a lista de dicionários contendo os dados dos cursos
    cursos = obter_cursos_db()
    
    # 2. Reseta a tabela
    #   Passo crítico: 
    #       Sem limpar (clear), se essa função for chamada novamente para recarregar a tela, as linhas se duplicarão indefinidamente.
    tabela_cursos.rows.clear()

    # 3. Itera sobre os dados brutos e os transforma em componentes visuais (DataRow)
    for c in cursos:
        linha = criar_linha_curso(
            contexto_tabela,
            c.get("id"),
            
            # Utiliza o segundo parâmetro do método .get() como valor padrão (fallback)
            #   Evita que o app quebre se o campo estiver ausente no documento do Firestore.
            c.get("codigo", "S/C"), 
            c.get("nome", ""),
            c.get("departamento", ""),
            c.get("coordenador", ""),
        )
        
        # Injeta a linha criada diretamente na estrutura interna da tabela
        tabela_cursos.rows.append(linha)
        
    # 4. Avisa o Flet que a árvore de componentes foi modificada e precisa ser redesenhada na tela.
    atualizar_interface_callback()