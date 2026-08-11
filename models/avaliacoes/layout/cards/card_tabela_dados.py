import flet as ft
from typing import Optional
from components.core.constants.constants import TEXTO_PRINCIPAL
from components.widgets.card.card_base import criar_card_base
from models.avaliacoes.core.export_csv import exportar_csv
from models.avaliacoes.layout.cards.card_tabela_linha import criar_linha
from database.services.firestore_avaliacoes import obter_respostas_tabela # Chama o serviço que encapsula a lógica de conexão com o banco de dados

def criar_card_tabela_dados(layout, page: ft.Page, expand: bool = True, height: Optional[int] = None) -> ft.Container:
    """Cartão com uma tabela de respostas recentes e função de exportação."""
    
    '''
    Faz a consulta ao banco de dados no exato momento em que o card é gerado.
        Ao entrar nesta tela, o sistema sempre trará os dados mais recentes salvos na nuvem.
    '''
    dados_tabela = obter_respostas_tabela()
    
    # Constrói o widget nativo de tabela de dados do Flet
    tabela_dados = ft.DataTable(
        expand=True,
        # Definição estrutural do cabeçalho das colunas
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Data")),
            ft.DataColumn(ft.Text("Curso")),
            ft.DataColumn(ft.Text("Eixo Avaliado")),
            ft.DataColumn(ft.Text("Nota")),
            ft.DataColumn(ft.Text("Comentário")),
        ],
        rows=[criar_linha(item) for item in dados_tabela], # Mapeia a lista de dicionários vindas do Firestore diretamente para a função visual que constrói cada linha (Row)
    )

    # Estrutura a interface interna contida no card
    conteudo = ft.Column(
        expand=True,
        controls=[
            # Primeira linha interna: Título alinhado à esquerda, Botão à direita (SPACE_BETWEEN)
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text("Respostas Recentes (Raw Data)", size=18, weight="bold", color=layout.cores[TEXTO_PRINCIPAL]),           
                    
                    # Botão de exportação
                    ft.ElevatedButton(
                        "Exportar CSV",
                        icon=ft.Icons.DOWNLOAD,
                        bgcolor=ft.Colors.BLUE_700,
                        color=ft.Colors.WHITE,
                        on_click=lambda e: exportar_csv(page, dados_tabela),
                    ),
                ],
            ),
            ft.Divider(color=ft.Colors.GREY_200), # Linha sutil separando o cabeçalho da área dos dados
            ft.Column(expand=True, scroll=ft.ScrollMode.AUTO, controls=[tabela_dados]), # Envelopa a tabela em uma Coluna com scroll automático, garantindo que o card não estoure visualmente os limites da página se houver muitas linhas
        ],
    )

    return criar_card_base(layout.cores, conteudo, expand=expand, height=height) # Delega a finalização visual para uma Factory externa (criar_card_base) que vai aplicar as sombras, bordas e os cantos arredondados padronizados do tema