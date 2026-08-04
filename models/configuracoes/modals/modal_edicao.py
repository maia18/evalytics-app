import flet as ft
from typing import Callable
from utils.services.indicadores.indicadores_repository import atualizar_indicador
from models.configuracoes.core.estado_indicadores import EstadoIndicadores

# Permite reescrever os metadados textuais básicos de um indicador
def criar_modal_edicao(
    page: ft.Page,
    estado: EstadoIndicadores,
    abrir_pasta: Callable[[str], None],
) -> tuple[ft.AlertDialog, ft.TextField, ft.TextField, Callable]:
    campo_titulo = ft.TextField(label="Título", border_color=ft.Colors.BLUE_200)
    campo_descricao = ft.TextField(label="Descrição", multiline=True, border_color=ft.Colors.BLUE_200)
    
    # Persiste as alterações de título/descrição do indicador
    def salvar_edicao(e: ft.ControlEvent) -> None:
        atualizar_indicador(
            estado.item_alvo.get("titulo"),
            estado.item_alvo.get("eixo"),
            campo_titulo.value or "",
            campo_descricao.value or "",
        )
        page.snack_bar = ft.SnackBar(ft.Text("Indicador atualizado!", color=ft.Colors.GREEN))
        page.snack_bar.open = True
        modal.open = False
        abrir_pasta(estado.pasta_titulo)
        page.update()

    modal = ft.AlertDialog(
        title=ft.Text("Editar Indicador", size=20, weight="bold"),
        content=ft.Column(width=400, height=200, spacing=15, controls=[campo_titulo, campo_descricao]),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: setattr(modal, "open", False)),
            ft.ElevatedButton("Salvar", bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE, on_click=salvar_edicao),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    # Seta o item alvo, pré-preenche os campos com os dados atuais e exibe o modal
    def abrir_modal_edicao(e: ft.ControlEvent, item: dict) -> None:
        estado.definir_item_alvo(item)
        campo_titulo.value = item.get("titulo", "")
        campo_descricao.value = item.get("descricao", "")

        if modal not in page.overlay:
            page.overlay.append(modal)
        modal.open = True
        page.update()

    return modal, campo_titulo, campo_descricao, abrir_modal_edicao