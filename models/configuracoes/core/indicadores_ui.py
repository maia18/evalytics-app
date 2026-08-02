import flet as ft
from typing import Callable

def criar_linha_indicador(
    item: dict,
    abrir_modal_criterios: Callable[..., None],
    abrir_modal_edicao: Callable[..., None],
    preparar_exclusao: Callable[[dict], None],
) -> ft.Container:
    """Cria o card retangular (linha) para representar um único indicador cadastrado na lista."""

    cor_status = ft.Colors.GREEN_600 if item.get("status") == "ATIVO" else ft.Colors.AMBER_600 # Define a cor de destaque (verde ou amarelo) dependendo do status do indicador.

    return ft.Container(
        padding=15, bgcolor=ft.Colors.WHITE, border_radius=8,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color=ft.Colors.BLACK12),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                # Container do texto, consome espaço disponível com expand=True e reage a cliques
                ft.Container(
                    content=ft.Text(item["titulo"], size=15, weight="w500", color=ft.Colors.BLUE_700),
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


def criar_pasta_indicador(titulo: str, qtd: int, abrir_pasta: Callable[[str], None]) -> ft.Container:
    """Cria um grande botão com visual de 'Pasta' para agrupar indicadores de um mesmo eixo na visualização raiz."""
    return ft.Container(
        bgcolor="#F4F6F9", border_radius=8, padding=20,
        ink=True,  # Adiciona Efeito visual de 'ripple' interativo
        on_click=lambda e: abrir_pasta(titulo),
        content=ft.Row(
            spacing=15,
            controls=[
                ft.Icon(ft.Icons.FOLDER, color=ft.Colors.BLUE_700, size=28),
                ft.Column(
                    spacing=2,
                    controls=[
                        ft.Text(titulo, size=16, weight="bold", color=ft.Colors.BLACK87),
                        ft.Text(f"{qtd} indicadores", size=13, color=ft.Colors.BLACK54),
                    ],
                ),
            ],
        ),
    )