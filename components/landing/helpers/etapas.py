import flet as ft
from components.core.constants.constants import (
    COR_TEXTO_TITULO,
    COR_TEXTO_SECUNDARIO,
    COR_PRIMARIA,
)

def criar_etapa(numero: str, titulo: str, descricao: str) -> ft.Row:
    """
    Cria um item visual de etapa utilizado para apresentar fluxos, processos ou instruções na Landing Page.

        Cada etapa é composta por:

            - Indicador numérico;
            - Título da etapa;
            - Descrição resumida.
    """

    return ft.Row(
        spacing=15,  # Espaçamento entre o indicador numérico e o conteúdo textual.
        vertical_alignment=ft.CrossAxisAlignment.CENTER, # Mantém todos os elementos alinhados verticalmente.
        controls=[

            # =================================================
            # INDICADOR DA ETAPA
            # =================================================
            
            # Exibe o número da etapa dentro de um bloco visual destacado.
            ft.Container(
                width=38,
                height=38,
                border_radius=8, # Bordas arredondadas para manter consistência visual com a identidade da aplicação.

                # Utiliza uma versão suavizada da cor primária para destacar sem competir visualmente com o restante do conteúdo.
                bgcolor=ft.Colors.with_opacity(
                    0.10,
                    COR_PRIMARIA,
                ),

                alignment=ft.Alignment.CENTER,

                content=ft.Text(
                    numero,
                    size=12,
                    weight=ft.FontWeight.BOLD,
                    color=COR_PRIMARIA,
                ),
            ),

            # =================================================
            # CONTEÚDO DA ETAPA
            # =================================================
            
            # Agrupa título e descrição.
            ft.Column(
                spacing=2,
                expand=True, # Permite que o conteúdo utilize toda a largura disponível.
                
                controls=[

                    # Título principal da etapa.
                    ft.Text(
                        titulo,
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=COR_TEXTO_TITULO,
                    ),

                    # Texto complementar explicando o objetivo ou funcionamento da etapa.
                    ft.Text(
                        descricao,
                        size=12,
                        color=COR_TEXTO_SECUNDARIO,
                    ),
                ],
            ),
        ],
    )