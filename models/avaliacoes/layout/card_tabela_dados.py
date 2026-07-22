import flet as ft
from models.avaliacoes.core.export_csv import exportar_csv
from components.core.constants.constants import *

def criar_card_tabela_dados(layout, page):
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

    return ft.Container(
        expand=True,
        bgcolor=layout.cores[CARD],
        padding=25,
        border_radius=10,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color="black12"),
        content=ft.Column(
            expand=True,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text("Respostas Recentes (Raw Data)", size=18, weight="bold", color=layout.cores[TEXTO_PRINCIPAL]),
                        # CORREÇÃO APLICADA AQUI: Uso do lambda para capturar o evento e passar a page
                        ft.ElevatedButton("Exportar CSV", icon=ft.Icons.DOWNLOAD, bgcolor="blue700", color="white", on_click=lambda e: exportar_csv(page))
                    ]
                ),
                ft.Divider(color="grey200"),
                ft.Column(expand=True, scroll=ft.ScrollMode.AUTO, controls=[tabela_dados])
            ]
        )
    )