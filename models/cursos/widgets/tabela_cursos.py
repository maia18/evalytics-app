import flet as ft
from dataclasses import dataclass
from typing import Callable, Optional
from database.services.firestore_courses import excluir_curso_db

@dataclass
class ContextoTabelaCursos:
    """
    Agrupa as dependências compartilhadas para construir e operar uma linha da tabela de cursos.

    NOTA ARQUITETURAL: 
        Um único objeto de contexto, criado uma vez e reutilizado em todos os pontos que criam linhas (carga inicial e cadastro via modal), evita que algum desses pontos passe por engano um conjunto de campos ou um estado diferente do que é realmente compartilhado com o modal de edição, simplificando as assinaturas de funções.
    """
    page: ft.Page
    tabela_cursos: ft.DataTable
    atualizar_interface: Callable[[], None]
    modal_editar: ft.AlertDialog
    campos_edit: dict[str, ft.TextField]
    estado: dict

def criar_linha_curso(contexto: ContextoTabelaCursos, doc_id: Optional[str], codigo: str, nome: str, depto: str, coord: str,) -> ft.DataRow:
    """Gera uma linha oficial (DataRow) para a tabela, com os callbacks de editar e excluir já acoplados."""
    
    # Destaca em verde o código da linha se ele acabou de ser criado e não está salvo com código definitivo no banco
    txt_codigo = ft.Text(codigo, color=ft.Colors.GREEN if codigo == "NOVO" else ft.Colors.BLACK, weight="bold")
    txt_nome = ft.Text(nome, weight="bold")
    txt_depto = ft.Text(depto)
    txt_coord = ft.Text(coord)

    linha = ft.DataRow(
        cells=[
            ft.DataCell(txt_codigo),
            ft.DataCell(txt_nome),
            ft.DataCell(txt_depto),
            ft.DataCell(txt_coord),
            ft.DataCell(ft.Row()),  # Preenchida abaixo com os ícones de ação de Editar e Excluir
        ]
    )

    def acao_deletar(e: ft.ControlEvent) -> None:
        """Remove o curso permanentemente no Firestore e, em caso de sucesso, retira a linha visual da tabela."""
        
        sucesso = excluir_curso_db(doc_id)
        if sucesso:
            # Remove a linha atual utilizando a lista do contexto
            contexto.tabela_cursos.rows.remove(linha)
            contexto.page.update()

            contexto.atualizar_interface() # Recalcula as estatísticas (KPIs superiores) já que uma linha foi removida

    def acao_editar(e: ft.ControlEvent) -> None:
        """Carrega os dados específicos desta linha nos campos do modal de edição e o exibe para o usuário."""
        
        # Joga os valores atuais (que podem ser recém-editados) para dentro do Input do Modal
        contexto.campos_edit["nome"].value = txt_nome.value
        contexto.campos_edit["departamento"].value = txt_depto.value
        contexto.campos_edit["coordenador"].value = txt_coord.value

        # Salva no dicionário global de estado qual linha e ID o modal vai atacar na hora de dar o "Salvar"
        contexto.estado["linha_atual"] = linha
        contexto.estado["id_firebase"] = doc_id

        # Processo padrão do Flet para renderizar modais flutuantes
        if contexto.modal_editar not in contexto.page.overlay:
            contexto.page.overlay.append(contexto.modal_editar)
            
        contexto.modal_editar.open = True
        contexto.page.update()

    # Injeta os botões na última DataCell reservada acima
    linha.cells[4].content = ft.Row([
        ft.IconButton(icon=ft.Icons.EDIT, icon_color=ft.Colors.BLUE_700, tooltip="Editar", on_click=acao_editar),
        ft.IconButton(icon=ft.Icons.DELETE, icon_color=ft.Colors.RED_700, tooltip="Excluir", on_click=acao_deletar),
    ])

    return linha