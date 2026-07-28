import flet as ft 
from models.avaliacoes.core.export_csv import exportar_csv 
from components.core.constants.constants import * 

def criar_card_tabela_dados(layout, page): 
    """
    Constrói um cartão contendo uma tabela de dados (DataTable) com as respostas recentes e função de exportação.
    """
    
    # Cria a estrutura nativa de tabela do Flet
    tabela_dados = ft.DataTable( 
        expand=True, # Garante que a tabela ocupe o máximo de largura possível
        # Definição dos cabeçalhos das colunas
        columns=[ 
            ft.DataColumn(ft.Text("ID")), 
            ft.DataColumn(ft.Text("Data")), 
            ft.DataColumn(ft.Text("Curso")), 
            ft.DataColumn(ft.Text("Eixo Avaliado")), 
            ft.DataColumn(ft.Text("Nota")), 
            ft.DataColumn(ft.Text("Comentário")), 
        ], 
        # Preenchimento de dados fictícios para visualização estrutural
        rows=[ 
            ft.DataRow(cells=[ 
                ft.DataCell(ft.Text("RES-004", color="grey700")), 
                ft.DataCell(ft.Text("Hoje, 10:20")), 
                ft.DataCell(ft.Text("Engenharia")), 
                ft.DataCell(ft.Text("Inovação")), 
                ft.DataCell(ft.Text("4.8", weight="bold", color="green700")), # Destaque positivo para nota alta
                ft.DataCell(ft.Icon(ft.Icons.CHAT_BUBBLE_OUTLINE, size=18, color="blue700", tooltip="Uso excelente de simulações em Python.")), # Dica visual oculta via tooltip
            ]), 
            ft.DataRow(cells=[ 
                ft.DataCell(ft.Text("RES-003", color="grey700")), 
                ft.DataCell(ft.Text("Hoje, 09:15")), 
                ft.DataCell(ft.Text("Administração")), 
                ft.DataCell(ft.Text("Didática")), 
                ft.DataCell(ft.Text("5.0", weight="bold", color="green700")), 
                ft.DataCell(ft.Text("-", color="grey400")), # Ausência de comentário
            ]), 
            ft.DataRow(cells=[ 
                ft.DataCell(ft.Text("RES-002", color="grey700")), 
                ft.DataCell(ft.Text("Ontem, 15:45")), 
                ft.DataCell(ft.Text("Engenharia")), 
                ft.DataCell(ft.Text("Infraestrutura")), 
                ft.DataCell(ft.Text("3.0", weight="bold", color="orange700")), # Destaque de alerta para nota mediana/baixa
                ft.DataCell(ft.Icon(ft.Icons.CHAT_BUBBLE_OUTLINE, size=18, color="blue700", tooltip="Laboratórios precisam de atualização.")), 
            ]), 
        ] 
    ) 

    # Encapsula a tabela dentro do padrão visual de "Card"
    return ft.Container( 
        expand=True, # O card deve preencher o espaço vertical restante da tela
        bgcolor=layout.cores[CARD], # Fundo adaptativo
        padding=20, # Reduzido de 25 para 20
        border_radius=10, 
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color="black12"), 
        content=ft.Column( 
            expand=True, # A coluna de conteúdo acompanha a expansão do container
            controls=[ 
                # Cabeçalho da tabela com título e botão de exportação
                ft.Row( 
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN, 
                    controls=[ 
                        ft.Text("Respostas Recentes (Raw Data)", size=18, weight="bold", color=layout.cores[TEXTO_PRINCIPAL]), 
                        # Chama função externa de utilitário repassando a page para manipular UI (como diálogos de salvamento)
                        ft.ElevatedButton("Exportar CSV", icon=ft.Icons.DOWNLOAD, bgcolor="blue700", color="white", on_click=lambda e: exportar_csv(page)) 
                    ] 
                ), 
                ft.Divider(color="grey200"), # Separação visual
                # Envolve a tabela de dados em uma Coluna com rolagem habilitada
                # Isso impede que dados excessivos quebrem o layout caso o número de linhas passe a altura da tela
                ft.Column(expand=True, scroll=ft.ScrollMode.AUTO, controls=[tabela_dados]) 
            ] 
        ) 
    )