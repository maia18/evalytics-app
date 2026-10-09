import flet as ft
from typing import Callable
from components.core.constants.constants import (
    BORDA,
    COR_PRIMARIA,
    TEXTO_PRINCIPAL,
    SUCESSO,
    PERIGO,
)
from models.configuracoes.widgets.estado_indicadores import EstadoIndicadores
from utils.services.indicadores.indicadores_repository import atualizar_indicador

def criar_modal_edicao(
    page: ft.Page,
    estado: EstadoIndicadores,
    abrir_pasta: Callable[[str], None],
    cores: dict[str, str],
) -> tuple[ft.AlertDialog, ft.TextField, ft.TextField, Callable]:
    """Permite editar título e descrição de um indicador."""

    campo_titulo = ft.TextField(
        label="Título",
        border_color=cores[BORDA],
    )

    campo_descricao = ft.TextField(
        label="Descrição",
        multiline=True,
        border_color=cores[BORDA],
    )

    def salvar_edicao(e: ft.ControlEvent) -> None:
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

        novo_titulo = (campo_titulo.value or "").strip()
        nova_descricao = (campo_descricao.value or "").strip()

        if not novo_titulo:
            page.snack_bar = ft.SnackBar(
                ft.Text(
                    "Informe o título do indicador."
                ),
                bgcolor=cores[PERIGO],
            )
            page.snack_bar.open = True
            page.update()
            return

        sucesso = atualizar_indicador(
            indicador_id,
            novo_titulo,
            nova_descricao,
        )

        if not sucesso:
            page.snack_bar = ft.SnackBar(
                ft.Text(
                    "Não foi possível atualizar o indicador. "
                    "Verifique se o título já está sendo utilizado."
                ),
                bgcolor=cores[PERIGO],
            )
            page.snack_bar.open = True
            page.update()
            return

        page.snack_bar = ft.SnackBar(
            ft.Text("Indicador atualizado!"),
            bgcolor=cores[SUCESSO],
        )
        page.snack_bar.open = True

        modal.open = False

        # Reconsulta o Firestore ao reconstruir a pasta.
        abrir_pasta(estado.pasta_titulo)

        page.update()

    modal = ft.AlertDialog(
        title=ft.Text(
            "Editar Indicador",
            size=20,
            weight=ft.FontWeight.BOLD,
            color=cores[TEXTO_PRINCIPAL],
        ),
        content=ft.Column(
            width=400,
            height=200,
            spacing=15,
            controls=[
                campo_titulo,
                campo_descricao,
            ],
        ),
        actions=[
            ft.TextButton(
                "Cancelar",
                on_click=lambda e: setattr(modal, "open", False),
            ),
            ft.ElevatedButton(
                "Salvar",
                bgcolor=cores[COR_PRIMARIA],
                color=ft.Colors.WHITE,
                on_click=salvar_edicao,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def abrir_modal_edicao(
        e: ft.ControlEvent,
        item: dict,
    ) -> None:
        estado.definir_item_alvo(item)

        campo_titulo.value = item.get("titulo", "")
        campo_descricao.value = item.get("descricao", "")

        if modal not in page.overlay:
            page.overlay.append(modal)

        modal.open = True
        page.update()

    return modal, campo_titulo, campo_descricao, abrir_modal_edicao