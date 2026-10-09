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
from utils.services.indicadores.indicadores_repository import adicionar_indicador

def criar_modal_novo(
    page: ft.Page,
    estado: EstadoIndicadores,
    abrir_pasta: Callable[[str], None],
    cores: dict[str, str],
) -> tuple[ft.AlertDialog, ft.TextField, ft.TextField, Callable]:
    """Cria o modal de cadastro de um novo indicador."""

    campo_titulo = ft.TextField(
        label="Título do Indicador",
        border_color=cores[BORDA],
    )

    campo_desc = ft.TextField(
        label="Descrição",
        multiline=True,
        border_color=cores[BORDA],
    )

    def salvar_novo(e: ft.ControlEvent) -> None:
        titulo = (campo_titulo.value or "").strip()
        descricao = (campo_desc.value or "").strip()
        eixo = estado.pasta_eixo

        # Validação básica
        if not titulo:
            page.snack_bar = ft.SnackBar(
                ft.Text("Informe o título do indicador."),
                bgcolor=cores[PERIGO],
            )
            page.snack_bar.open = True
            page.update()
            return

        if eixo is None:
            page.snack_bar = ft.SnackBar(
                ft.Text("Não foi possível identificar o eixo do indicador."),
                bgcolor=cores[PERIGO],
            )
            page.snack_bar.open = True
            page.update()
            return

        sucesso = adicionar_indicador(
            titulo,
            eixo,
            descricao,
        )

        if not sucesso:
            page.snack_bar = ft.SnackBar(
                ft.Text(
                    "Não foi possível criar o indicador. "
                    "Verifique se já existe um indicador com esse título."
                ),
                bgcolor=cores[PERIGO],
            )
            page.snack_bar.open = True
            page.update()
            return

        # Limpa os campos somente após a gravação bem-sucedida.
        campo_titulo.value = ""
        campo_desc.value = ""

        page.snack_bar = ft.SnackBar(
            ft.Text("Novo indicador criado!"),
            bgcolor=cores[SUCESSO],
        )
        page.snack_bar.open = True

        modal.open = False

        # Reconsulta o Firestore ao reconstruir a pasta.
        abrir_pasta(estado.pasta_titulo)

        page.update()

    modal = ft.AlertDialog(
        title=ft.Text(
            "Novo Indicador",
            size=18,
            weight=ft.FontWeight.BOLD,
            color=cores[TEXTO_PRINCIPAL],
        ),
        content=ft.Column(
            width=400,
            height=200,
            spacing=15,
            controls=[
                campo_titulo,
                campo_desc,
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
                on_click=salvar_novo,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def abrir_modal_novo() -> None:
        if modal not in page.overlay:
            page.overlay.append(modal)

        modal.open = True
        page.update()

    return modal, campo_titulo, campo_desc, abrir_modal_novo