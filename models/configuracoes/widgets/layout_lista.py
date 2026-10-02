import flet as ft
from typing import Callable

from models.configuracoes.widgets.indicadores_ui import (
    criar_linha_indicador,
)

from models.configuracoes.widgets.estado_indicadores import (
    EstadoIndicadores,
)

from utils.services.indicadores.indicadores_repository import (
    listar_indicadores_por_eixo,
)


def criar_layout_lista(
    page: ft.Page,
    estado: EstadoIndicadores,
    titulo_pasta: str,
    eixo_id: int,
    callback_voltar: Callable[[], None],
    cores: dict[str, str],
) -> ft.Column:

    lista_da_pasta = listar_indicadores_por_eixo(eixo_id)

    controles_lista: list[ft.Control] = [
        ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            on_click=lambda _: callback_voltar(),
                        ),
                        ft.Text(
                            titulo_pasta,
                            size=22,
                            weight=ft.FontWeight.BOLD,
                            color=cores["#111827"],
                        ),
                    ]
                ),
                ft.ElevatedButton(
                    "Novo Indicador",
                    icon=ft.Icons.ADD,
                    bgcolor=cores["#4809F4"],
                    color=ft.Colors.WHITE,
                    on_click=lambda e: estado.abrir_modal_novo(),
                ),
            ],
        ),
        ft.Divider(
            height=20,
            color=ft.Colors.TRANSPARENT,
        ),
    ]

    if not lista_da_pasta:
        controles_lista.append(
            ft.Container(
                padding=30,
                alignment=ft.Alignment.CENTER,
                content=ft.Text(
                    "Nenhum indicador cadastrado neste eixo.",
                    color=cores["#5F6368"],
                ),
            )
        )

    for item in lista_da_pasta:
        controles_lista.append(
            criar_linha_indicador(
                item,
                lambda e, i=item: estado.abrir_modal_criterios(
                    e,
                    i,
                ),
                lambda e, i=item: estado.abrir_modal_edicao(
                    e,
                    i,
                ),
                lambda i=item: estado.preparar_exclusao(i),
                cores,
            )
        )

    return ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        spacing=15,
        controls=controles_lista,
    )