import flet as ft
from database.services.firestore_courses import atualizar_curso_db

def criar_modal_edit(page, estado, campos_edit, atualizar_interface):
    def fechar_modal(e):
        modal.open = False
        page.update()

    def salvar_edicao(e):
        linha_em_edicao = estado["linha_atual"]
        id_banco = estado["id_firebase"]
        nome = campos_edit["nome"].value
        depto = campos_edit["departamento"].value
        coord = campos_edit["coordenador"].value

        if linha_em_edicao and id_banco:
            sucesso = atualizar_curso_db(id_banco, nome, depto, coord)
            if sucesso:
                linha_em_edicao.cells[1].content.value = nome
                linha_em_edicao.cells[2].content.value = depto
                linha_em_edicao.cells[3].content.value = coord
        fechar_modal(e)
        atualizar_interface()

    modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Editar Curso", size=20, weight="bold"),
        content=ft.Column(width=400, height=220, spacing=15, controls=list(campos_edit.values())),
        actions=[
            ft.TextButton("Cancelar", on_click=fechar_modal, style=ft.ButtonStyle(color="red700")),
            ft.ElevatedButton("Atualizar", on_click=salvar_edicao, bgcolor="blue700", color="white"),
        ],
    )

    return modal
