""" Importações """  
import flet as ft
from components.layout.responsive.responsive import ResponsiveLayout
from models.avaliacoes.core.export_csv import exportar_csv
from components.core.constants import *

def ViewAvaliacoes(page: ft.Page, mudar_tela):
    
    """
    View responsável pela tela de Avaliações.
    Inclui exportação de dados, cards de controle e tabela de respostas.
    """
    
    # Criar o layout responsivo
    layout = ResponsiveLayout(
        page, 
        titulo_pagina="Avaliações", 
        subtitulo="Acompanhe respostas e métricas em tempo real.", 
        mudar_tela=mudar_tela
    )

    """ COMPONENTES VISUAIS """
    
    # --- Card 1: Controle do Ciclo de Avaliação ---
    status_ciclo = ft.Container(
        content=ft.Text("EM ANDAMENTO", color="white", size=12, weight="bold"),
        bgcolor="green600",
        padding=8, 
        border_radius=15
    )

    card_controle_ciclo = ft.Container(
        bgcolor=layout.cores["CARD"],
        padding=25,
        border_radius=10,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color="black12"),
        content=ft.Column(
            spacing=20,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Column(
                            spacing=2,
                            controls=[
                                ft.Text("Ciclo de Avaliação Ativo", size=14, color="grey600"),
                                ft.Row([ft.Text("Semestre 2026.1", size=22, weight="bold", color=PRIMARIA), status_ciclo])
                            ]
                        ),
                        ft.Row(
                            spacing=10,
                            controls=[
                                ft.ElevatedButton(
                                    "Visão do Usuário", 
                                    icon=ft.Icons.OPEN_IN_NEW, 
                                    bgcolor="blue700", 
                                    color="white",
                                    on_click=lambda _: mudar_tela("/formulario") 
                                ),
                                ft.ElevatedButton(
                                    "Copiar Link", 
                                    icon=ft.Icons.CONTENT_COPY, 
                                    bgcolor="blue50", 
                                    color="blue700",
                                    on_click=lambda _: setattr(page.snack_bar, 'open', True) or setattr(page.snack_bar, 'content', ft.Text("Link copiado para a área de transferência!")) or page.update()
                                )
                            ]
                        )
                    ]
                ),
                ft.Divider(color="grey200"),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text("342 respostas coletadas até o momento.", size=14, color="black87"),
                        ft.TextButton("Encerrar Ciclo", icon=ft.Icons.STOP_CIRCLE, style=ft.ButtonStyle(color="red700"))
                    ]
                )
            ]
        )
    )

    # --- Card 2: Tabela de Dados Brutos (Raw Data) ---
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
        rows=[
            # Exemplo de linhas com dados simulados
            ft.DataRow(cells=[
                ft.DataCell(ft.Text("RES-004", color="grey700")),
                ft.DataCell(ft.Text("Hoje, 10:20")),
                ft.DataCell(ft.Text("Engenharia")),
                ft.DataCell(ft.Text("Inovação")),
                ft.DataCell(ft.Text("4.8", weight="bold", color="green700")),
                ft.DataCell(ft.Icon(ft.Icons.CHAT_BUBBLE_OUTLINE, size=18, color="blue700", tooltip="Uso excelente de simulações em Python.")),
            ]),
            ft.DataRow(cells=[
                ft.DataCell(ft.Text("RES-003", color="grey700")),
                ft.DataCell(ft.Text("Hoje, 09:15")),
                ft.DataCell(ft.Text("Administração")),
                ft.DataCell(ft.Text("Didática")),
                ft.DataCell(ft.Text("5.0", weight="bold", color="green700")),
                ft.DataCell(ft.Text("-", color="grey400")),
            ]),
            ft.DataRow(cells=[
                ft.DataCell(ft.Text("RES-002", color="grey700")),
                ft.DataCell(ft.Text("Ontem, 15:45")),
                ft.DataCell(ft.Text("Engenharia")),
                ft.DataCell(ft.Text("Infraestrutura")),
                ft.DataCell(ft.Text("3.0", weight="bold", color="orange700")),
                ft.DataCell(ft.Icon(ft.Icons.CHAT_BUBBLE_OUTLINE, size=18, color="blue700", tooltip="Laboratórios precisam de atualização.")),
            ]),
        ]
    )

    card_tabela_dados = ft.Container(
        expand=True,
        bgcolor=layout.cores["CARD"],
        padding=25,
        border_radius=10,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color="black12"),
        content=ft.Column(
            expand=True,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text("Respostas Recentes (Raw Data)", size=18, weight="bold", color=layout.cores["TEXTO_PRINCIPAL"]),
                        ft.ElevatedButton("Exportar CSV", icon=ft.Icons.DOWNLOAD, bgcolor="blue700", color="white", on_click=exportar_csv)
                    ]
                ),
                ft.Divider(color="grey200"),
                ft.Column(expand=True, scroll=ft.ScrollMode.AUTO, controls=[tabela_dados])
            ]
        )
    )

    """ CONTEÚDO PRINCIPAL """
    
    conteudo = ft.Column(
        expand=True,
        spacing=20,
        controls=[
            ft.Column(
                spacing=5,
                controls=[
                    ft.Text("Gestão de Ciclos e Respostas", size=28, weight="bold", color=layout.cores["TEXTO_PRINCIPAL"]),
                    ft.Text("Monitore campanhas ativas e extraia os dados brutos das avaliações.", size=16, color="grey"),
                ]
            ),
            card_controle_ciclo,
            card_tabela_dados
        ]
    )
    
    layout.add_content(conteudo)    
    return layout.criar_view("/avaliacoes")