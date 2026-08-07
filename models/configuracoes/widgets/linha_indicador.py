from typing import Callable
import flet as ft

def criar_linha_indicador(item: dict, abrir_modal_criterios: Callable[..., None], abrir_modal_edicao: Callable[..., None], preparar_exclusao: Callable[[dict], None]) -> ft.Container:
    """Cria o card retangular (linha) para representar um único indicador cadastrado na lista."""

    # Define a cor de destaque (verde ou amarelo) dependendo do status do indicador.
    cor_status = ft.Colors.GREEN_600 if item.get("status") == "ATIVO" else ft.Colors.AMBER_600

    return ft.Container(
        padding=15, 
        bgcolor=ft.Colors.WHITE, 
        border_radius=8,
        shadow=ft.BoxShadow(
            spread_radius=1, 
            blur_radius=5, 
            color=ft.Colors.BLACK12
        ),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                # Container do texto, consome espaço disponível com expand=True e reage a cliques
                ft.Container(
                    content=ft.Text(
                        item["titulo"], 
                        size=15, 
                        weight="w500", 
                        color=ft.Colors.BLUE_700
                    ),
                    expand=True,
                    on_click=lambda e, i=item: abrir_modal_criterios(e, i),
                ),
                # Tag / Badge visual de Status
                ft.Container(
                    bgcolor=cor_status, padding=5, border_radius=4,
                    content=ft.Text(item.get("status", "ATIVO"), size=12, color=ft.Colors.WHITE, weight="bold"),
                ),
                # Grupo de botões de Ações rápidas (Editar metadados ou Excluir permanentemente)
                ft.Row([
                    ft.IconButton(icon=ft.Icons.EDIT, icon_color=ft.Colors.BLUE_700, tooltip="Editar", on_click=lambda e, i=item: abrir_modal_edicao(e, i)),
                    ft.IconButton(icon=ft.Icons.DELETE, icon_color=ft.Colors.RED_700, tooltip="Excluir", on_click=lambda e: preparar_exclusao(item)),
                ]),
            ],
        ),
    )