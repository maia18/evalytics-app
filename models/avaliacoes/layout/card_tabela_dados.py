import flet as ft
from typing import Optional
from components.core.constants.constants import TEXTO_PRINCIPAL
from components.widgets.card.card_base import criar_card_base
from models.avaliacoes.core.export_csv import exportar_csv
from models.avaliacoes.layout.card_tabela_linha import criar_linha
from database.services.firestore_avaliacoes import obter_respostas_tabela # Chama o serviço do banco de dados

def criar_card_tabela_dados(
    layout,
    page: ft.Page,
    expand: bool = True,
    height: Optional[int] = None,
) -> ft.Container:
    """Cartão com uma tabela de respostas recentes e função de exportação."""
    
    # Faz a consulta ao banco de dados no momento em que o card é gerado
    dados_tabela = obter_respostas_tabela()
    
    tabela_dados = ft.DataTable(
        expand=True,
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Data")),
            ft.DataColumn(ft.Text("Curso")),
            ft.DataColumn(ft.Text("Eixo Avaliado")),
            ft.DataColumn(ft.Text("Nota")),
            ft.DataColumn(ft.Text("Comentário")),
        ],
        rows=[criar_linha(item) for item in dados_tabela], # Mapeia as linhas dinâmicas vindas do Firestore diretamente para a função visual
    ) 

    conteudo = ft.Column(
        expand=True,
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text("Respostas Recentes (Raw Data)", size=18, weight="bold", color=layout.cores[TEXTO_PRINCIPAL]),
                    ft.ElevatedButton(
                        "Exportar CSV", icon=ft.Icons.DOWNLOAD,
                        bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE,
                        on_click=lambda e: exportar_csv(page, dados_tabela),
                    ),
                ],
            ),
            ft.Divider(color=ft.Colors.GREY_200),
            ft.Column(expand=True, scroll=ft.ScrollMode.AUTO, controls=[tabela_dados]),
        ],
    )

    return criar_card_base(layout.cores, conteudo, expand=expand, height=height)