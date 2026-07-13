""" Importações """  
import flet as ft
from components.responsive_layout import ResponsiveLayout

def ViewRelatorios(page: ft.Page, mudar_tela):
    """
    Tela de Relatórios do sistema Evalytics.
    Permite filtrar dados por semestre e eixo, visualizar resultados consolidados
    e exportar em diferentes formatos.
    """
    
    # Criar o layout responsivo
    layout = ResponsiveLayout(page, "Relatórios e Exportações", "Gere visualizações dinâmicas e exporte resultados.")

    # === CONTEÚDO PRINCIPAL ===
    conteudo = ft.Column(
        expand=True,
        controls=[
            # Cabeçalho
            ft.Text("Relatórios e Exportações", size=28, weight="bold", color=layout.COR_TEXTO_PRINCIPAL),
            ft.Text("Gere visualizações dinâmicas, analise os critérios e exporte os resultados.", size=16, color="grey"),
            ft.Divider(height=30, color="transparent"),
            
            # Barra de filtros e ações
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Row(
                        spacing=15,
                        controls=[
                            ft.Dropdown(
                                label="Semestre",
                                options=[ft.dropdown.Option("2025.2"), ft.dropdown.Option("2026.1")],
                                width=150,
                                border_color="blue200",
                                dense=True
                            ),
                            ft.Dropdown(
                                label="Eixo Avaliativo",
                                options=[ft.dropdown.Option("Todos"), ft.dropdown.Option("Infraestrutura"), ft.dropdown.Option("Corpo Docente")],
                                width=200,
                                border_color="blue200",
                                dense=True
                            ),
                        ]
                    ),
                    ft.Row(
                        spacing=10,
                        controls=[
                            ft.ElevatedButton("Exportar CSV", icon=ft.Icons.TABLE_VIEW, bgcolor="green700", color="white"),
                            ft.ElevatedButton("Gerar Documento (PDF)", icon=ft.Icons.PICTURE_AS_PDF, bgcolor="red700", color="white"),
                        ]
                    )
                ]
            ),
            ft.Divider(height=20, color="transparent"),
            
            # Container para resultados
            ft.Container(
                expand=True,
                bgcolor=layout.COR_CARD,
                border_radius=10,
                padding=25,
                shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color="black12"),
                content=ft.Column(
                    controls=[
                        ft.Text("Resultados Consolidados", size=18, weight="bold", color=layout.COR_TEXTO_PRINCIPAL),
                        ft.Divider(height=10, color="transparent"),
                        ft.ListView(
                            expand=True,
                            controls=[
                                ft.DataTable(
                                    heading_row_color="blue50",
                                    columns=[
                                        ft.DataColumn(ft.Text("Semestre", weight="bold")),
                                        ft.DataColumn(ft.Text("Infraestrutura", weight="bold")),
                                        ft.DataColumn(ft.Text("Didática", weight="bold")),
                                        ft.DataColumn(ft.Text("Atendimento", weight="bold")),
                                        ft.DataColumn(ft.Text("Material", weight="bold")),
                                        ft.DataColumn(ft.Text("Inovação", weight="bold")),
                                    ],
                                    rows=[
                                        ft.DataRow(cells=[
                                            ft.DataCell(ft.Text("2025.2")),
                                            ft.DataCell(ft.Text("4.8")),
                                            ft.DataCell(ft.Text("4.5")),
                                            ft.DataCell(ft.Text("4.0")),
                                            ft.DataCell(ft.Text("4.2")),
                                            ft.DataCell(ft.Text("4.7")),
                                        ]),
                                        ft.DataRow(cells=[
                                            ft.DataCell(ft.Text("2026.1")),
                                            ft.DataCell(ft.Text("Aguardando", color="grey")),
                                            ft.DataCell(ft.Text("-")),
                                            ft.DataCell(ft.Text("-")),
                                            ft.DataCell(ft.Text("-")),
                                            ft.DataCell(ft.Text("-")),
                                        ]),
                                    ],
                                )
                            ]
                        )
                    ]
                )
            )
        ]
    )
    
    # Adicionar conteúdo ao layout
    layout.add_content(conteudo)
    
    # Retornar a view
    return layout.criar_view("/relatorios")