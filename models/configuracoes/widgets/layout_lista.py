import flet as ft
from typing import Callable
from models.configuracoes.widgets.indicadores_ui import criar_linha_indicador
from models.configuracoes.widgets.estado_indicadores import EstadoIndicadores
from utils.services.indicadores.indicadores_repository import listar_indicadores_por_eixo

def criar_layout_lista(page: ft.Page, estado: EstadoIndicadores, titulo_pasta: str, eixo_id: int, callback_voltar: Callable[[], None]) -> ft.Column:
    """Gera a interface interna de uma pasta contendo a lista de indicadores cadastrados."""
    
    # Acessa os dados reais no repositório de JSON (ou banco futuro)
    lista_da_pasta = listar_indicadores_por_eixo(eixo_id) 

    # Inicia os controles visuais com o cabeçalho (Botão voltar, Título e Botão de Novo)
    controles_lista: list[ft.Control] = [
        ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row([
                    ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda _: callback_voltar()),
                    ft.Text(titulo_pasta, size=22, weight="bold", color=ft.Colors.BLACK87),
                ]),
                ft.ElevatedButton(
                    "Novo Indicador", icon=ft.Icons.ADD, bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE,
                    on_click=lambda e: estado.abrir_modal_novo(),
                ),
            ],
        ),
        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
    ]

    # Adiciona cada item gerado à lista de renderização visual repassando os Callbacks Globais do estado
    for item in lista_da_pasta:
        controles_lista.append(
            criar_linha_indicador(
                item,
                lambda e, i=item: estado.abrir_modal_criterios(e, i),
                lambda e, i=item: estado.abrir_modal_edicao(e, i),
                lambda i=item: estado.preparar_exclusao(i),
            )
        )
        
    return ft.Column(expand=True, scroll=ft.ScrollMode.AUTO, spacing=15, controls=controles_lista) # Retorna a coluna configurada com scroll automático pronta para ser injetada na tela