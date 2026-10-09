import flet as ft
from typing import Callable
from components.core.constants.constants import (
    CARD,
    BORDA,
    COR_PRIMARIA,
    SUCESSO,
    AVISO,
)

def criar_linha_indicador(
    item: dict,
    abrir_modal_criterios: Callable[..., None],
    abrir_modal_edicao: Callable[..., None],
    preparar_exclusao: Callable[[dict], None],
    cores: dict[str, str],
) -> ft.Container:

    cor_status = (
        cores[SUCESSO]
        if item.get("status") == "ATIVO"
        else cores[AVISO]
    )

    return ft.Container(
        padding=15,
        bgcolor=cores[CARD],

        border=ft.Border(
            top=ft.BorderSide(1, cores[BORDA]),
            bottom=ft.BorderSide(1, cores[BORDA]),
            left=ft.BorderSide(1, cores[BORDA]),
            right=ft.BorderSide(1, cores[BORDA]),
        ),

        border_radius=8,

        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Container(
                    expand=True,
                    content=ft.Text(
                        item["titulo"],
                        size=15,
                        weight=ft.FontWeight.W_500,
                        color=cores[COR_PRIMARIA],
                    ),
                    on_click=lambda e, i=item: abrir_modal_criterios(e, i),
                ),

                ft.Container(
                    bgcolor=cor_status,
                    padding=5,
                    border_radius=4,
                    content=ft.Text(
                        item.get("status", "ATIVO"),
                        size=12,
                        color=ft.Colors.WHITE,
                        weight=ft.FontWeight.BOLD,
                    ),
                ),

                ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.EDIT,
                            icon_color=cores[COR_PRIMARIA],
                            tooltip="Editar",
                            on_click=lambda e, i=item: abrir_modal_edicao(e, i),
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            icon_color=ft.Colors.RED_700,
                            tooltip="Excluir",
                            on_click=lambda e, i=item: preparar_exclusao(i),
                        ),
                    ],
                ),
            ],
        ),
    )