import flet as ft
from typing import Callable
from components.core.constants.constants import (
    COR_PRIMARIA,
    ESTILO_BOTAO_CANCELAR,
)
from database.services.cursos.firestore_courses import atualizar_curso_db
from models.cursos.modals.modal_utils import fechar_modal

def criar_modal_edit(
    page: ft.Page,
    estado: dict,
    campos_edit: dict[str, ft.Control],
    atualizar_interface: Callable[[], None],
    cores: dict[str, str],
) -> ft.AlertDialog:
    """Constrói a janela de edição de curso, usando `estado` para saber qual linha visual e ID do banco editar."""

    def salvar_edicao(e: ft.ControlEvent) -> None:
        """Puxa as referências exatas salvas pelo botão de 'Editar' da linha da tabela"""
        linha_em_edicao = estado["linha_atual"]
        id_banco = estado["id_firebase"]

        nome = campos_edit["nome"].value
        depto = campos_edit["departamento"].value
        coord = campos_edit["coordenador"].value
        ativo = campos_edit["status"].value == "ATIVO"

        nome = (nome or "").strip()
        depto = (depto or "").strip()
        campos_edit["nome"].error_text = None
        campos_edit["departamento"].error_text = None
        if not nome or not depto:
            if not nome:
                campos_edit["nome"].error_text = "Informe o nome do curso."
            if not depto:
                campos_edit["departamento"].error_text = "Informe o departamento."
            page.update()
            return

        if linha_em_edicao and id_banco:
            sucesso = atualizar_curso_db(id_banco, nome, depto, coord, ativo)
            if sucesso:
                linha_em_edicao.cells[1].content.value = nome
                linha_em_edicao.cells[2].content.value = depto
                linha_em_edicao.cells[3].content.value = coord
                linha_em_edicao.cells[4].content.value = ativo
                linha_em_edicao.cells[4].content.label = "Ativo" if ativo else "Inativo"

                fechar_modal(page, modal)
                atualizar_interface()

    modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Editar Curso", size=20, weight="bold"),
        content=ft.Column(
            width=500,
            height=330,
            spacing=12,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                ft.Text("Nome e departamento são obrigatórios."),
                *list(campos_edit.values()),
            ],
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: fechar_modal(page, modal), style=ESTILO_BOTAO_CANCELAR),
            ft.ElevatedButton(
                "Atualizar",
                on_click=salvar_edicao,
                bgcolor=cores[COR_PRIMARIA],
                color=ft.Colors.WHITE,
            )
        ],
    )

    return modal
