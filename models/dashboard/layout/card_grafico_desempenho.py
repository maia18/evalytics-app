import flet as ft

# Importa a "casca" padrão que criamos para manter o design consistente
from components.widgets.card.card_base import criar_card_base
from components.core.constants.constants import TEXTO_PRINCIPAL, COR_PRIMARIA

# IMPORTAÇÃO CHAVE: Traz a função que calcula as médias do Firestore
from database.services.firestore_dashboard import obter_medias_dashboard


def _criar_barra_indicador(titulo: str, nota: float) -> ft.Column:
    """
    Componente auxiliar que desenha uma única barra de progresso para um indicador.
    Ele converte a nota de 0 a 5 em uma porcentagem de 0.0 a 1.0 para o Flet.
    """
    # Calcula a porcentagem (ex: nota 4.0 de 5.0 vira 0.8)
    valor_percentual = nota / 5.0

    return ft.Column(
        spacing=4,
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    # Transforma a chave do banco (ex: 'infraestrutura') em título com inicial maiúscula
                    ft.Text(titulo.capitalize(), size=14, weight="w500"),
                    ft.Text(f"{nota} / 5.0", size=14, weight="bold", color=COR_PRIMARIA),
                ],
            ),
            # A barra de progresso visual
            ft.ProgressBar(
                value=valor_percentual,
                color=COR_PRIMARIA,
                bgcolor=ft.Colors.GREY_200,
                height=8,
            ),
        ],
    )


def criar_card_grafico_desempenho(layout) -> ft.Container:
    """
    Card principal que busca os dados do Firestore e constrói o gráfico de desempenho geral.
    """
    # 1. Busca as médias diretamente do banco de dados
    medias = obter_medias_dashboard()

    # 2. Tratamento de Estado Vazio (Zero avaliações no banco)
    if not medias:
        conteudo_vazio = ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Icon(ft.Icons.BAR_CHART, size=48, color=ft.Colors.GREY_400),
                ft.Text("Nenhuma avaliação registrada ainda.", color=ft.Colors.GREY_500),
            ]
        )
        return criar_card_base(layout.cores, content=conteudo_vazio, expand=True)

    # 3. Tratamento de Estado Preenchido (Monta as barras dinamicamente)
    barras_controles = []
    
    # Itera sobre o dicionário retornado pelo banco (ex: campo='didatica', nota=4.5)
    for campo, nota in medias.items():
        barras_controles.append(_criar_barra_indicador(titulo=campo, nota=nota))

    # 4. Monta a estrutura final do Card
    conteudo = ft.Column(
        spacing=20,
        controls=[
            ft.Text("Desempenho por Eixo", size=18, weight="bold", color=layout.cores[TEXTO_PRINCIPAL]),
            ft.Divider(color=ft.Colors.GREY_200),
            
            # Envelopa as barras em uma coluna secundária
            ft.Column(
                spacing=16,
                controls=barras_controles,
            )
        ]
    )

    # Retorna usando a casca padrão para manter a sombra e as bordas arredondadas
    return criar_card_base(layout.cores, conteudo, expand=True)