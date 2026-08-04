from typing import Callable

import flet as ft

from database.services.firestore_courses import atualizar_curso_db
from models.cursos.modals.modal_utils import ESTILO_BOTAO_CANCELAR, fechar_modal

def criar_modal_edit(
    page: ft.Page,
    estado: dict,
    campos_edit: dict[str, ft.TextField],
    atualizar_interface: Callable[[], None],
) -> ft.AlertDialog:
    """Constrói a janela de edição de curso, usando `estado` para saber qual linha visual e ID do banco editar."""

    def salvar_edicao(e: ft.ControlEvent) -> None:
        # Puxa as referências exatas salvas pelo botão de 'Editar' da linha da tabela
        linha_em_edicao = estado["linha_atual"]
        id_banco = estado["id_firebase"]

        nome = campos_edit["nome"].value
        depto = campos_edit["departamento"].value
        coord = campos_edit["coordenador"].value

        if linha_em_edicao and id_banco:
            sucesso = atualizar_curso_db(id_banco, nome, depto, coord)
            if sucesso:
                # Modifica apenas a linha visual (DataRow) que está sendo apontada
                # Reflete os novos textos nas células visuais diretamente (célula 0, o código, não é editável aqui)
                linha_em_edicao.cells[1].content.value = nome
                linha_em_edicao.cells[2].content.value = depto
                linha_em_edicao.cells[3].content.value = coord

        fechar_modal(page, modal)
        atualizar_interface()

    modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Editar Curso", size=20, weight="bold"),
        content=ft.Column(width=400, height=220, spacing=15, controls=list(campos_edit.values())),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: fechar_modal(page, modal), style=ESTILO_BOTAO_CANCELAR),
            ft.ElevatedButton("Atualizar", on_click=salvar_edicao, bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE),
        ],
    )

    return modal