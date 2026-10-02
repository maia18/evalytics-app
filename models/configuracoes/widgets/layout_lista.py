import flet as ft
from typing import Callable
from components.core.constants.constants import (
    TEXTO_PRINCIPAL,
    COR_PRIMARIA,
    BORDA,
)
from models.configuracoes.widgets.indicadores_ui import criar_linha_indicador
from models.configuracoes.widgets.estado_indicadores import EstadoIndicadores

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
    """
    Gera a interface interna de uma "pasta" (Eixo),
    exibindo a lista de indicadores cadastrados nela.
    """

    # 1. Busca os indicadores vinculados ao eixo
    lista_da_pasta = listar_indicadores_por_eixo(eixo_id)

    # 2. Construção da lista de controles
    controles_lista: list[ft.Control] = [
        # Cabeçalho
        ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                # Esquerda: voltar + título
                ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            icon_color=cores[TEXTO_PRINCIPAL],
                            on_click=lambda _: callback_voltar(),
                        ),
                        ft.Text(
                            titulo_pasta,
                            size=22,
                            weight=ft.FontWeight.BOLD,
                            color=cores[TEXTO_PRINCIPAL],
                        ),
                    ],
                ),

                # Direita: novo indicador
                ft.ElevatedButton(
                    "Novo Indicador",
                    icon=ft.Icons.ADD,
                    bgcolor=cores[COR_PRIMARIA],
                    color=ft.Colors.WHITE,
                    on_click=lambda e: estado.abrir_modal_novo(),
                ),
            ],
        ),

        # Separador
        ft.Divider(
            height=20,
            color=cores[BORDA],
        ),
    ]

    # 3. Adiciona dinamicamente os indicadores
    for item in lista_da_pasta:
        controles_lista.append(
            criar_linha_indicador(
                item,
                lambda e, i=item: estado.abrir_modal_criterios(e, i),
                lambda e, i=item: estado.abrir_modal_edicao(e, i),
                lambda i=item: estado.preparar_exclusao(i),
                cores,
            )
        )

    # 4. Retorna o layout completo
    return ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        spacing=15,
        controls=controles_lista,
    )