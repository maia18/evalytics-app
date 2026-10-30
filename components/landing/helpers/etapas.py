import flet as ft
from components.landing.palette import TEXTO_CLARO, TEXTO_CLARO_SECUNDARIO, ROXO

def criar_etapa(
    numero: str,
    titulo: str,
    descricao: str,
    opacidade: float = 1.0,
) -> ft.Row:
    """
    Cria um item visual de etapa com indicador numérico preenchido.

        Cada etapa é composta por:

            - Indicador numérico colorido;
            - Título da etapa;
            - Descrição resumida.

        O parâmetro 'opacidade' controla a intensidade da cor de fundo
        do indicador, permitindo criar efeitos de gradiente visual
        entre etapas consecutivas.
    """

    return ft.Row(
        spacing=14,
        vertical_alignment=ft.CrossAxisAlignment.START,
        controls=[

            # =================================================
            # INDICADOR DA ETAPA
            # =================================================

            ft.Container(
                width=36,
                height=36,
                border_radius=10,
                bgcolor=ft.Colors.with_opacity(
                    opacidade,
                    ROXO,
                ),
                alignment=ft.Alignment.CENTER,
                content=ft.Text(
                    numero,
                    size=13,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                ),
            ),

            # =================================================
            # CONTEÚDO DA ETAPA
            # =================================================

            ft.Column(
                spacing=2,
                expand=True,
                controls=[
                    ft.Text(
                        titulo,
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=TEXTO_CLARO,
                    ),
                    ft.Text(
                        descricao,
                        size=12,
                        color=TEXTO_CLARO_SECUNDARIO,
                    ),
                ],
            ),
        ],
    )
