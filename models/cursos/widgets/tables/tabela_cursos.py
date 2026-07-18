import flet as ft
from database.services.firestore_courses import excluir_curso_db

def criar_linha_curso(page, tabela_cursos, atualizar_interface, modal_editar, campos_edit, estado, doc_id, codigo, nome, depto, coord):
    txt_codigo = ft.Text(codigo, color="green" if codigo == "NOVO" else "black", weight="bold")
    txt_nome = ft.Text(nome, weight="bold")
    txt_depto = ft.Text(depto)
    txt_coord = ft.Text(coord)

    linha = ft.DataRow(
        cells=[
            ft.DataCell(txt_codigo),
            ft.DataCell(txt_nome),
            ft.DataCell(txt_depto),
            ft.DataCell(txt_coord),
            ft.DataCell(ft.Row())
        ]
    )

    def acao_deletar(e):
        sucesso = excluir_curso_db(doc_id)
        if sucesso:
            tabela_cursos.rows.remove(linha)
            page.update()
            atualizar_interface()

    def acao_editar(e):
        campos_edit["nome"].value = txt_nome.value
        campos_edit["departamento"].value = txt_depto.value
        campos_edit["coordenador"].value = txt_coord.value
        estado["linha_atual"] = linha
        estado["id_firebase"] = doc_id
        if modal_editar not in page.overlay:
            page.overlay.append(modal_editar)
        modal_editar.open = True
        page.update()

    linha.cells[4].content = ft.Row([
        ft.IconButton(icon=ft.Icons.EDIT, icon_color="blue700", tooltip="Editar", on_click=acao_editar),
        ft.IconButton(icon=ft.Icons.DELETE, icon_color="red700", tooltip="Excluir", on_click=acao_deletar)
    ])

    return linha
