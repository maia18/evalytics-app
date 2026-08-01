from typing import Callable

import flet as ft

from utils.services.sessions.indicadores_repository import adicionar_indicador
from models.configuracoes.core.estado_indicadores import EstadoIndicadores


def criar_modal_novo(
    page: ft.Page,
    estado: EstadoIndicadores,
    abrir_pasta: Callable[[str], None],
) -> tuple[ft.AlertDialog, ft.TextField, ft.TextField, Callable]:
    """Cria o modal de cadastro de um novo indicador."""
    campo_titulo = ft.TextField(label="Título do Indicador", border_color=ft.Colors.BLUE_200)
    campo_desc = ft.TextField(label="Descrição", multiline=True, border_color=ft.Colors.BLUE_200)

    def salvar_novo(e: ft.ControlEvent) -> None:
        """Cria e persiste um novo indicador no eixo da pasta atualmente aberta."""
        adicionar_indicador(campo_titulo.value or "", estado.pasta_eixo, campo_desc.value or "")

        campo_titulo.value = ""
        campo_desc.value = ""

        page.snack_bar = ft.SnackBar(ft.Text("Novo indicador criado!", color=ft.Colors.GREEN))
        page.snack_bar.open = True
        modal.open = False
        abrir_pasta(estado.pasta_titulo)
        page.update()

    modal = ft.AlertDialog(
        title=ft.Text("Novo Indicador", size=18, weight="bold"),
        content=ft.Column(width=400, height=200, spacing=15, controls=[campo_titulo, campo_desc]),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: setattr(modal, "open", False)),
            ft.ElevatedButton("Salvar", bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE, on_click=salvar_novo),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def abrir_modal_novo() -> None:
        """Exibe o modal com os campos limpos, pronto para um novo cadastro."""
        if modal not in page.overlay:
            page.overlay.append(modal)
        modal.open = True
        page.update()

    return modal, campo_titulo, campo_desc, abrir_modal_novo