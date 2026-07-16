import flet as ft
from database.services.firestore_courses import adicionar_curso_db

def criar_modal_add(page, tabela_cursos, criar_linha_curso, atualizar_interface, campos_add):
    def fechar_modal(e):
        modal.open = False
        page.update()

    def salvar_curso(e):
        nome = campos_add["nome"].value
        depto = campos_add["departamento"].value
        coord = campos_add["coordenador"].value
        codigo_novo = "NOVO"

        if nome:
            novo_id = adicionar_curso_db(codigo_novo, nome, depto, coord)
            if novo_id:
                nova_linha = criar_linha_curso(page, tabela_cursos, atualizar_interface, None, campos_add, {}, novo_id, codigo_novo, nome, depto, coord)
                tabela_cursos.rows.append(nova_linha)
                for campo in campos_add.values():
                    campo.value = ""
                fechar_modal(e)
                atualizar_interface()

    modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Cadastrar Novo Curso", size=20, weight="bold"),
        content=ft.Column(width=400, height=220, spacing=15, controls=list(campos_add.values())),
        actions=[
            ft.TextButton("Cancelar", on_click=fechar_modal, style=ft.ButtonStyle(color="red700")),
            ft.ElevatedButton("Salvar", on_click=salvar_curso, bgcolor="blue700", color="white"),
        ],
    )

    def abrir_modal_add(e):
        if modal not in page.overlay:
            page.overlay.append(modal)
        modal.open = True
        page.update()

    return abrir_modal_add
