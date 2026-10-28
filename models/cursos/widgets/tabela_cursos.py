import flet as ft
from dataclasses import dataclass
from typing import Callable, Optional

from components.core.constants.constants import (
    COR_PRIMARIA,
    PERIGO,
    SUCESSO,
    TEXTO_PRINCIPAL,
    TEXTO_SECUNDARIO,
)
from database.services.cursos.firestore_courses import (
    atualizar_status_curso_db,
    excluir_curso_db,
)


@dataclass
class ContextoTabelaCursos:
    page: ft.Page
    tabela_cursos: ft.DataTable
    atualizar_interface: Callable[[], None]
    modal_editar: ft.AlertDialog
    campos_edit: dict[str, ft.Control]
    estado: dict
    cores: dict[str, str]


def criar_linha_curso(
    contexto: ContextoTabelaCursos,
    doc_id: Optional[str],
    codigo: str,
    nome: str,
    depto: str,
    coord: str,
    ativo: bool = True,
    quantidade_avaliacoes: int = 0,
) -> ft.DataRow:
    """Cria uma linha do catálogo com dados, status e ações."""
    codigo_limpo = str(codigo or "").strip()
    if codigo_limpo.upper() in {"NOVO", "S/C", ""}:
        codigo_limpo = "Sem código"

    texto_codigo = ft.Text(
        codigo_limpo,
        color=contexto.cores[TEXTO_SECUNDARIO]
        if codigo_limpo == "Sem código"
        else contexto.cores[TEXTO_PRINCIPAL],
        weight="w500",
    )
    texto_nome = ft.Text(nome or "—", weight="bold", color=contexto.cores[TEXTO_PRINCIPAL])
    texto_departamento = ft.Text(depto or "—", color=contexto.cores[TEXTO_PRINCIPAL])
    texto_coordenador = ft.Text(coord or "—", color=contexto.cores[TEXTO_PRINCIPAL])
    controle_status = ft.Switch(
        value=ativo,
        label="Ativo" if ativo else "Inativo",
        tooltip="Ativar ou inativar curso",
        active_color=contexto.cores[SUCESSO],
    )

    linha = ft.DataRow(
        cells=[
            ft.DataCell(texto_codigo),
            ft.DataCell(texto_nome),
            ft.DataCell(texto_departamento),
            ft.DataCell(texto_coordenador),
            ft.DataCell(controle_status),
            ft.DataCell(ft.Text(str(quantidade_avaliacoes))),
            ft.DataCell(ft.Row()),
        ]
    )

    def confirmar_exclusao(e=None) -> None:
        confirmacao.open = False
        if excluir_curso_db(doc_id):
            contexto.atualizar_interface()
        else:
            contexto.page.update()

    confirmacao = ft.AlertDialog(
        modal=True,
        title=ft.Text("Excluir curso"),
        content=ft.Text(
            f"Deseja excluir '{nome}'? Esta ação remove o curso do cadastro."
        ),
        actions=[
            ft.TextButton(
                "Cancelar",
                on_click=lambda e: _fechar_confirmacao(contexto.page, confirmacao),
            ),
            ft.ElevatedButton(
                "Excluir",
                bgcolor=contexto.cores[PERIGO],
                color=ft.Colors.WHITE,
                on_click=confirmar_exclusao,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def acao_excluir(e: ft.ControlEvent) -> None:
        if confirmacao not in contexto.page.overlay:
            contexto.page.overlay.append(confirmacao)
        confirmacao.open = True
        contexto.page.update()

    def acao_editar(e: ft.ControlEvent) -> None:
        contexto.campos_edit["nome"].value = nome or ""
        contexto.campos_edit["departamento"].value = depto or ""
        contexto.campos_edit["coordenador"].value = coord or ""
        contexto.campos_edit["status"].value = (
            "ATIVO" if controle_status.value else "INATIVO"
        )
        contexto.campos_edit["nome"].error_text = None
        contexto.campos_edit["departamento"].error_text = None
        contexto.estado["id_firebase"] = doc_id
        contexto.estado["linha_atual"] = linha
        if contexto.modal_editar not in contexto.page.overlay:
            contexto.page.overlay.append(contexto.modal_editar)
        contexto.modal_editar.open = True
        contexto.page.update()

    def alterar_status(e: ft.ControlEvent) -> None:
        novo_status = bool(controle_status.value)
        sucesso = atualizar_status_curso_db(doc_id, novo_status)
        if sucesso:
            controle_status.label = "Ativo" if novo_status else "Inativo"
            contexto.atualizar_interface()
        else:
            controle_status.value = not novo_status
            contexto.page.update()

    controle_status.on_change = alterar_status

    linha.cells[6].content = ft.Row(
        spacing=2,
        controls=[
            ft.IconButton(
                icon=ft.Icons.EDIT_OUTLINED,
                icon_color=contexto.cores[COR_PRIMARIA],
                tooltip="Editar curso",
                on_click=acao_editar,
            ),
            ft.IconButton(
                icon=ft.Icons.DELETE_OUTLINE,
                icon_color=contexto.cores[PERIGO],
                tooltip="Excluir curso",
                on_click=acao_excluir,
            ),
        ],
    )
    return linha


def _fechar_confirmacao(page: ft.Page, dialogo: ft.AlertDialog) -> None:
    dialogo.open = False
    page.update()
