from typing import Callable

import flet as ft

from utils.services.sessions.indicadores_repository import excluir_indicador
from models.configuracoes.core.estado_indicadores import EstadoIndicadores


def criar_modal_exclusao(
    page: ft.Page,
    estado: EstadoIndicadores,
    abrir_pasta: Callable[[str], None],
) -> tuple[ft.AlertDialog, Callable]:
    """Painel de confirmação ('Tem certeza?') que exclui um indicador."""

    def confirmar_exclusao(e: ft.ControlEvent) -> None:
        """Remove o indicador alvo e persiste a alteração."""
        excluir_indicador(estado.item_alvo.get("titulo"), estado.item_alvo.get("eixo"))

        page.snack_bar = ft.SnackBar(ft.Text("Indicador removido!", color=ft.Colors.RED))
        page.snack_bar.open = True
        modal.open = False
        abrir_pasta(estado.pasta_titulo)
        page.update()

    modal = ft.AlertDialog(
        title=ft.Text("Confirmar Exclusão", size=18, weight="bold", color=ft.Colors.RED_700),
        content=ft.Text("Tem certeza que deseja excluir este indicador?"),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: setattr(modal, "open", False)),
            ft.ElevatedButton("Excluir", bgcolor=ft.Colors.RED_700, color=ft.Colors.WHITE, on_click=confirmar_exclusao),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def preparar_exclusao(item: dict) -> None:
        """Captura o item selecionado antes de exibir a confirmação de exclusão."""
        estado.definir_item_alvo(item)
        if modal not in page.overlay:
            page.overlay.append(modal)
        modal.open = True
        page.update()

    return modal, preparar_exclusao