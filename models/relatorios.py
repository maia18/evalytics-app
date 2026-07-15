""" Importações """  
import flet as ft
from components.layout.responsive import ResponsiveLayout

def ViewRelatorios(page: ft.Page, mudar_tela):
    """
    Tela de Relatórios do sistema Evalytics.
    Permite filtrar dados por semestre e eixo, visualizar resultados consolidados
    e exportar em diferentes formatos.
    """
    
    layout = ResponsiveLayout(
        page, 
        titulo_pagina="Relatórios e Exportações", 
        subtitulo="Gere visualizações dinâmicas e exporte resultados.", 
        mudar_tela=mudar_tela
    )
    
    # === 0. DEFINIÇÕES DE ESTILO (Necessário para a borda) ===
    borda_container = ft.Border(
        top=ft.BorderSide(1, layout.COR_BORDA),
        bottom=ft.BorderSide(1, layout.COR_BORDA),
        left=ft.BorderSide(1, layout.COR_BORDA),
        right=ft.BorderSide(1, layout.COR_BORDA),
    )
    
    # === 1. COMPONENTES DE FILTRO ===
    dropdown_semestre = ft.Dropdown(
        label="Semestre",
        options=[ft.dropdown.Option("2026.1"), ft.dropdown.Option("2025.2")],
        width=200,
        dense=True
    )

    dropdown_eixo = ft.Dropdown(
        label="Eixo Avaliativo",
        options=[
            ft.dropdown.Option("Infraestrutura"),
            ft.dropdown.Option("Didática"),
            ft.dropdown.Option("Atendimento")
        ],
        width=200,
        dense=True
    )

    # === 2. SEÇÃO ÚNICA DE FILTROS E AÇÕES ===
    secao_filtros = ft.Container(
        bgcolor=layout.COR_CARD,
        padding=20,
        border_radius=8,
        border=borda_container,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row([dropdown_semestre, dropdown_eixo], spacing=10),
                ft.Row([
                    ft.ElevatedButton("Exportar CSV", icon=ft.Icons.TABLE_VIEW, bgcolor="green700", color="white"),
                    ft.ElevatedButton("Gerar Documento (PDF)", icon=ft.Icons.PICTURE_AS_PDF, bgcolor="red700", color="white")
                ], spacing=10)
            ]
        )
    )

    # === CONTEÚDO PRINCIPAL (Limpo e sem duplicidade) ===
    conteudo = ft.Column(
        expand=True,
        controls=[
            ft.Text("Relatórios e Exportações", size=28, weight="bold", color=layout.COR_TEXTO_PRINCIPAL),
            ft.Text("Gere visualizações dinâmicas, analise os critérios e exporte os resultados.", size=16, color="grey"),
            ft.Divider(height=30, color="transparent"),
            secao_filtros, # Filtros e ações em um único lugar
            ft.Divider(height=20, color="transparent"),
            
            # Container para resultados
            ft.Container(
                expand=True,
                bgcolor=layout.COR_CARD,
                padding=25,
                border=borda_container,
                border_radius=10,
                content=ft.Column(
                    controls=[
                        ft.Text("Resultados Consolidados", size=18, weight="bold", color=layout.COR_TEXTO_PRINCIPAL),
                        ft.DataTable(
                            heading_row_color=ft.Colors.BLUE_GREY_900 if page.theme_mode == ft.ThemeMode.DARK else "blue50",
                            columns=[
                                ft.DataColumn(ft.Text("Semestre", weight="bold", color=ft.Colors.ON_SURFACE)),
                                ft.DataColumn(ft.Text("Infraestrutura", weight="bold", color=ft.Colors.ON_SURFACE)),
                                ft.DataColumn(ft.Text("Didática", weight="bold", color=ft.Colors.ON_SURFACE)),
                                ft.DataColumn(ft.Text("Atendimento", weight="bold", color=ft.Colors.ON_SURFACE)),
                                ft.DataColumn(ft.Text("Material", weight="bold", color=ft.Colors.ON_SURFACE)),
                                ft.DataColumn(ft.Text("Inovação", weight="bold", color=ft.Colors.ON_SURFACE)),
                            ],
                            rows=[
                                ft.DataRow(cells=[
                                    ft.DataCell(ft.Text("2025.2", color=ft.Colors.ON_SURFACE)),
                                    ft.DataCell(ft.Text("4.8", color=ft.Colors.ON_SURFACE)),
                                    ft.DataCell(ft.Text("4.5", color=ft.Colors.ON_SURFACE)),
                                    ft.DataCell(ft.Text("4.0", color=ft.Colors.ON_SURFACE)),
                                    ft.DataCell(ft.Text("4.2", color=ft.Colors.ON_SURFACE)),
                                    ft.DataCell(ft.Text("4.7", color=ft.Colors.ON_SURFACE)),
                                    ]),
                                ft.DataRow(cells=[
                                    ft.DataCell(ft.Text("2026.1", color=ft.Colors.ON_SURFACE)),
                                    ft.DataCell(ft.Text("Aguardando", color=ft.Colors.ON_SURFACE)),
                                    ft.DataCell(ft.Text("-", color=ft.Colors.ON_SURFACE)),
                                    ft.DataCell(ft.Text("-", color=ft.Colors.ON_SURFACE)),
                                    ft.DataCell(ft.Text("-", color=ft.Colors.ON_SURFACE)),
                                    ft.DataCell(ft.Text("", color=ft.Colors.ON_SURFACE)),
                                    ]),
                            ],
                        )
                    ]
                )
            )
        ]
    )
    
    layout.add_content(conteudo)
    return layout.criar_view("/relatorios")