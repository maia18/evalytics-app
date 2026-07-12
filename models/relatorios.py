""" Importações """  
import flet as ft

def ViewRelatorios(page: ft.Page, mudar_tela):
    """
    Tela de Relatórios do sistema Evalytics.
    Permite filtrar dados por semestre e eixo, visualizar resultados consolidados
    e exportar em diferentes formatos.
    """

    # === 1. SIDEBAR (MENU LATERAL) ===
    estilo_botao_menu = ft.ButtonStyle(
        color={"":"white70", "hovered":"white"},
        bgcolor={"":"transparent", "hovered":"white10"},
        shape=ft.RoundedRectangleBorder(radius=8),
        padding=15,
        alignment=ft.alignment.Alignment(-1, 0) 
    )
    
    def sair(e):
        mudar_tela("/")  # Redireciona para tela inicial

    sidebar = ft.Container(
        width=260,
        bgcolor="blue900",
        padding=20,
        content=ft.Column(
            expand=True,
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.ANALYTICS, color="white", size=32),
                        ft.Text("Evalytics", size=24, weight="bold", color="white"),
                    ],
                    alignment=ft.MainAxisAlignment.START
                ),
                ft.Divider(color="white24", height=30),
                ft.TextButton("Visão Geral", icon=ft.Icons.HOME, on_click=lambda _: mudar_tela("/inicio"), style=estilo_botao_menu),
                ft.TextButton("Dashboard", icon=ft.Icons.DASHBOARD, on_click=lambda _: mudar_tela("/dashboard"), style=estilo_botao_menu),
                ft.TextButton("Avaliações", icon=ft.Icons.ASSIGNMENT, on_click=lambda _: mudar_tela("/avaliacoes"), style=estilo_botao_menu),
                ft.TextButton("Cursos", icon=ft.Icons.BOOK, on_click=lambda _: mudar_tela("/cursos"), style=estilo_botao_menu),
                ft.TextButton("Configurações", icon=ft.Icons.SETTINGS, on_click=lambda _: mudar_tela("/configuracoes"), style=estilo_botao_menu),
                ft.Container(expand=True), 
                ft.TextButton("Sair do Sistema", icon=ft.Icons.LOGOUT, style=estilo_botao_menu, on_click=sair)
            ]
        )
    )

    # === 2. CONTEÚDO PRINCIPAL ===
    area_conteudo = ft.Container(
        expand=True,
        padding=40,
        bgcolor="#F4F6F9",  # fundo claro para destacar os cartões
        content=ft.Column(
            expand=True,
            controls=[
                # Cabeçalho
                ft.Text("Relatórios e Exportações", size=28, weight="bold", color="black87"),
                ft.Text("Gere visualizações dinâmicas, analise os critérios e exporte os resultados.", size=16, color="black54"),
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
                    bgcolor="white",
                    border_radius=10,
                    padding=25,
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color="black12"),
                    content=ft.Column(
                        controls=[
                            ft.Text("Resultados Consolidados", size=18, weight="bold", color="black87"),
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
    )

    # === 3. VIEW FINAL ===
    return ft.View(
        route="/relatorios",
        padding=0,
        bgcolor="white",
        controls=[
            ft.Row(expand=True, spacing=0, controls=[sidebar, area_conteudo])
        ]
    )