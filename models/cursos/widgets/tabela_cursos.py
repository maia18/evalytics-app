import flet as ft 
from database.services.firestore_courses import excluir_curso_db 

def criar_linha_curso(page, tabela_cursos, atualizar_interface, modal_editar, campos_edit, estado, doc_id, codigo, nome, depto, coord): 
    """
    Gera uma linha de dados (DataRow) para a tabela, preenchida com as strings recebidas e acoplando os callbacks de editar e deletar.
    """
    # Prepara os textos. Cursos criados na sessão recebem cor verde na flag "NOVO"
    txt_codigo = ft.Text(codigo, color="green" if codigo == "NOVO" else "black", weight="bold") 
    txt_nome = ft.Text(nome, weight="bold") 
    txt_depto = ft.Text(depto) 
    txt_coord = ft.Text(coord) 

    # Constrói a linha base sem a coluna de ações
    linha = ft.DataRow( 
        cells=[ 
            ft.DataCell(txt_codigo), 
            ft.DataCell(txt_nome), 
            ft.DataCell(txt_depto), 
            ft.DataCell(txt_coord), 
            ft.DataCell(ft.Row()) # Container provisório para abrigar os ícones de ação logo abaixo
        ] 
    ) 

    def acao_deletar(e): 
        """Acionado ao clicar na Lixeira. Avisa o Firestore e retira a linha da lista visual."""
        sucesso = excluir_curso_db(doc_id) 
        if sucesso: 
            tabela_cursos.rows.remove(linha) # Dá um pop/remove na referência da linha
            page.update() 
            atualizar_interface() # Atualiza o "Total de Cursos" lá no topo

    def acao_editar(e): 
        """Seta as informações no modal de edição antes de ele ser aberto."""
        # Carrega os dados desta linha específica para dentro dos TextFields do Modal Edit
        campos_edit["nome"].value = txt_nome.value 
        campos_edit["departamento"].value = txt_depto.value 
        campos_edit["coordenador"].value = txt_coord.value 
        
        # Aponta o ponteiro central de estado para ESTA linha e ESTE doc_id
        estado["linha_atual"] = linha 
        estado["id_firebase"] = doc_id 
        
        # Insere e abre o modal
        if modal_editar not in page.overlay: 
            page.overlay.append(modal_editar) 
        modal_editar.open = True 
        page.update() 

    # Preenche a quinta célula com os botões de ação injetando as funções definidas acima
    linha.cells[4].content = ft.Row([ 
        ft.IconButton(icon=ft.Icons.EDIT, icon_color="blue700", tooltip="Editar", on_click=acao_editar), 
        ft.IconButton(icon=ft.Icons.DELETE, icon_color="red700", tooltip="Excluir", on_click=acao_deletar) 
    ]) 

    return linha 