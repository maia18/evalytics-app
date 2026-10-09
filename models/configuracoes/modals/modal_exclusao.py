import flet as ft
from typing import Callable
from components.core.constants.constants import (
    TEXTO_PRINCIPAL,
    PERIGO,
)
from models.configuracoes.widgets.estado_indicadores import EstadoIndicadores
from utils.services.indicadores.indicadores_repository import excluir_indicador

def criar_modal_exclusao(
    page: ft.Page,
    estado: EstadoIndicadores,
    abrir_pasta: Callable[[str], None],
    cores: dict[str, str],
) -> tuple[ft.AlertDialog, Callable]:
    """Cria o painel de confirmação de exclusão."""

    def confirmar_exclusao(e: ft.ControlEvent) -> None:
        indicador_id = estado.item_alvo.get("id")

        if not indicador_id:
            page.snack_bar = ft.SnackBar(
                ft.Text(
                    "Não foi possível identificar o indicador."
                ),
                bgcolor=cores[PERIGO],
            )
            page.snack_bar.open = True
            page.update()
            return

        sucesso = excluir_indicador(indicador_id)

        if not sucesso:
            page.snack_bar = ft.SnackBar(
                ft.Text(
                    "Não foi possível remover o indicador."
                ),
                bgcolor=cores[PERIGO],
            )
            page.snack_bar.open = True
            page.update()
            return

        page.snack_bar = ft.SnackBar(
            ft.Text("Indicador removido!"),
            bgcolor=cores[PERIGO],
        )
        page.snack_bar.open = True

        modal.open = False

        # Reconsulta o Firestore ao reconstruir a pasta.
        abrir_pasta(estado.pasta_titulo)
        page.update()

    modal = ft.AlertDialog(
        title=ft.Text(
            "Confirmar Exclusão",
            size=18,
            weight=ft.FontWeight.BOLD,
            color=cores[PERIGO],
        ),
        content=ft.Text(
            "Tem certeza que deseja excluir este indicador?",
            color=cores[TEXTO_PRINCIPAL],
        ),
        actions=[
            ft.TextButton(
                "Cancelar",
                on_click=lambda e: setattr(
                    modal,
                    "open",
                    False,
                ),
            ),
            ft.ElevatedButton(
                "Excluir",
                bgcolor=cores[PERIGO],
                color=ft.Colors.WHITE,
                on_click=confirmar_exclusao,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def preparar_exclusao(item: dict) -> None:
        estado.definir_item_alvo(item)

        if modal not in page.overlay:
            page.overlay.append(modal)

        modal.open = True
        page.update()

    return modal, preparar_exclusao