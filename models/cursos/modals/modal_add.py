from typing import Callable

import flet as ft

from database.services.firestore_courses import adicionar_curso_db
from models.cursos.widgets.tabela_cursos import ContextoTabelaCursos, criar_linha_curso
from models.cursos.modals.modal_utils import ESTILO_BOTAO_CANCELAR, abrir_modal, fechar_modal

# Código provisório exibido na coluna "Código" até a próxima sincronização com o banco
CODIGO_CURSO_PLACEHOLDER = "NOVO"

def criar_modal_add(contexto: ContextoTabelaCursos, campos_add: dict[str, ft.TextField]) -> Callable[[ft.ControlEvent], None]:
    """Constrói a janela de cadastro de curso e lida com a inserção no banco."""

    def salvar_curso(e: ft.ControlEvent) -> None:
        """Coleta o texto dos campos, grava no Firestore e reflete a nova linha na tabela dinamicamente."""
        nome = campos_add["nome"].value
        depto = campos_add["departamento"].value
        coord = campos_add["coordenador"].value

        if not nome:  # Validação básica: nome é obrigatório para prosseguir
            return

        novo_id = adicionar_curso_db(CODIGO_CURSO_PLACEHOLDER, nome, depto, coord)

        if novo_id:
            # Reaproveita o mesmo contexto compartilhado (modal de edição, campos e estado)
            # usado na carga inicial, para que editar esta linha nova logo em seguida funcione corretamente
            nova_linha = criar_linha_curso(contexto, novo_id, CODIGO_CURSO_PLACEHOLDER, nome, depto, coord)
            contexto.tabela_cursos.rows.append(nova_linha)

            # Limpa os campos após salvar para o próximo cadastro
            for campo in campos_add.values():
                campo.value = ""

            fechar_modal(contexto.page, modal)
            
            # Chama o método que recalcula a quantidade de cursos e departamentos no topo da tela
            contexto.atualizar_interface()

    modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Cadastrar Novo Curso", size=20, weight="bold"),
        content=ft.Column(width=400, height=220, spacing=15, controls=list(campos_add.values())),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: fechar_modal(contexto.page, modal), style=ESTILO_BOTAO_CANCELAR),
            ft.ElevatedButton("Salvar", on_click=salvar_curso, bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE),
        ],
    )

    def abrir_modal_add(e: ft.ControlEvent) -> None:
        abrir_modal(contexto.page, modal)

    return abrir_modal_add