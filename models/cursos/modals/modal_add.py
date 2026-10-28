import flet as ft
from typing import Callable
from components.core.constants.constants import (
    COR_PRIMARIA,
    ESTILO_BOTAO_CANCELAR,
)
from database.services.cursos.firestore_courses import (
    adicionar_curso_db,
    gerar_codigo_curso,
)
from models.cursos.widgets.tabela_cursos import ContextoTabelaCursos
from models.cursos.modals.modal_utils import (
    abrir_modal, 
    fechar_modal,
)

def criar_modal_add(
    contexto: ContextoTabelaCursos,
    campos_add: dict[str, ft.Control],
) -> Callable[[ft.ControlEvent], None]:
    """Constrói a janela de cadastro de curso e lida com a inserção no banco."""

    def salvar_curso(e: ft.ControlEvent) -> None:
        """Coleta o texto dos campos, grava no Firestore e reflete a nova linha na tabela dinamicamente."""
        
        nome = (campos_add["nome"].value or "").strip()
        depto = (campos_add["departamento"].value or "").strip()
        coord = (campos_add["coordenador"].value or "").strip()
        campos_add["nome"].error_text = None
        campos_add["departamento"].error_text = None

        if not nome or not depto:
            if not nome:
                campos_add["nome"].error_text = "Informe o nome do curso."
            if not depto:
                campos_add["departamento"].error_text = "Informe o departamento."
            contexto.page.update()
            return

        codigo = gerar_codigo_curso()
        ativo = campos_add["status"].value == "ATIVO"
        novo_id = adicionar_curso_db(codigo, nome, depto, coord, ativo)

        if novo_id:
            # Limpa os campos após salvar para o próximo cadastro
            for chave, campo in campos_add.items():
                campo.value = ""
                if chave == "status":
                    campo.value = "ATIVO"
                else:
                    campo.error_text = None

            fechar_modal(contexto.page, modal)
            contexto.atualizar_interface()

    modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Cadastrar Novo Curso", size=20, weight="bold"),
        content=ft.Column(
            width=500,
            height=330,
            spacing=12,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                ft.Text("Nome e departamento são obrigatórios. O código é gerado automaticamente."),
                *list(campos_add.values()),
            ],
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: fechar_modal(contexto.page, modal), style=ESTILO_BOTAO_CANCELAR),
            ft.ElevatedButton(
                "Salvar",
                on_click=salvar_curso,
                bgcolor=contexto.cores[COR_PRIMARIA],
                color=ft.Colors.WHITE,
            )
        ],
    )

    def abrir_modal_add(e: ft.ControlEvent) -> None:
        abrir_modal(contexto.page, modal)

    return abrir_modal_add
