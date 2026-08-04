import flet as ft

from components.widgets.card.card_base import criar_card_base
from components.core.constants.constants import TEXTO_PRINCIPAL, COR_PRIMARIA
from database.services.firestore_dashboard import obter_medias_dashboard


def _criar_barra_indicador(titulo: str, nota: float) -> ft.Column:
    """Desenha uma única barra de progresso para um indicador (nota de 0 a 5 convertida em 0.0-1.0)."""
    valor_percentual = nota / 5.0

    return ft.Column(
        spacing=4,
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text(titulo.capitalize(), size=14, weight="w500"),
                    ft.Text(f"{nota} / 5.0", size=14, weight="bold", color=COR_PRIMARIA),
                ],
            ),
            ft.ProgressBar(value=valor_percentual, color=COR_PRIMARIA, bgcolor=ft.Colors.GREY_200, height=8),
        ],
    )


def criar_card_grafico_desempenho(layout) -> ft.Container:
    """Card que busca as médias reais do Firestore e monta o gráfico de desempenho por eixo."""
    medias = obter_medias_dashboard()

    if not medias:
        conteudo_vazio = ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Icon(ft.Icons.BAR_CHART, size=48, color=ft.Colors.GREY_400),
                ft.Text("Nenhuma avaliação registrada ainda.", color=ft.Colors.GREY_500),
            ],
        )
        return criar_card_base(layout.cores, content=conteudo_vazio, expand=True)

    barras_controles = [
        _criar_barra_indicador(titulo=campo, nota=nota) for campo, nota in medias.items()
    ]

    conteudo = ft.Column(
        spacing=20,
        controls=[
            ft.Text("Desempenho por Eixo", size=18, weight="bold", color=layout.cores[TEXTO_PRINCIPAL]),
            ft.Divider(color=ft.Colors.GREY_200),
            ft.Column(spacing=16, controls=barras_controles),
        ],
    )

    return criar_card_base(layout.cores, conteudo, expand=True)