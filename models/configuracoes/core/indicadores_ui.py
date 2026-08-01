from typing import Callable

import flet as ft


def criar_linha_indicador(
    item: dict,
    abrir_modal_criterios: Callable[..., None],
    abrir_modal_edicao: Callable[..., None],
    preparar_exclusao: Callable[[dict], None],
) -> ft.Container:
    """Cria o card retangular (linha) para representar um único indicador cadastrado."""
    cor_status = ft.Colors.GREEN_600 if item.get("status") == "ATIVO" else ft.Colors.AMBER_600

    return ft.Container(
        padding=15,
        bgcolor=ft.Colors.WHITE,
        border_radius=8,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color=ft.Colors.BLACK12),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Container(
                    content=ft.Text(item["titulo"], size=15, weight="w500", color=ft.Colors.BLUE_700),
                    expand=True,
                    on_click=lambda e, i=item: abrir_modal_criterios(e, i),
                ),
                ft.Container(
                    bgcolor=cor_status, padding=5, border_radius=4,
                    content=ft.Text(item.get("status", "ATIVO"), size=12, color=ft.Colors.WHITE, weight="bold"),
                ),
                ft.Row([
                    ft.IconButton(icon=ft.Icons.EDIT, icon_color=ft.Colors.BLUE_700, tooltip="Editar", on_click=lambda e, i=item: abrir_modal_edicao(e, i)),
                    ft.IconButton(icon=ft.Icons.DELETE, icon_color=ft.Colors.RED_700, tooltip="Excluir", on_click=lambda e: preparar_exclusao(item)),
                ]),
            ],
        ),
    )


def criar_pasta_indicador(titulo: str, qtd: int, abrir_pasta: Callable[[str], None]) -> ft.Container:
    """Cria um grande botão com visual de 'Pasta' para agrupar indicadores de um mesmo eixo."""
    return ft.Container(
        bgcolor="#F4F6F9",  # Tom neutro específico deste componente, fora da paleta de tema
        border_radius=8,
        padding=20,
        ink=True,  # Efeito visual de 'ripple' nativo do Material Design
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