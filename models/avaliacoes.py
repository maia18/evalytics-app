import flet as ft # type: ignore
import csv
import os
from datetime import datetime

def ViewAvaliacoes(page: ft.Page, mudar_tela):
    
    # === 1. LÓGICA DE EXPORTAÇÃO DE DADOS ===
    def exportar_csv(e):
        # Dados simulados baseados na tabela
        dados_exportacao = [
            ["ID_Resposta", "Data_Hora", "Curso", "Eixo_Avaliado", "Nota_Geral", "Comentario"],
            ["RES-001", "2026-07-10 14:30", "Engenharia", "Didática", "4.5", "Ótima metodologia."],
            ["RES-002", "2026-07-10 15:45", "Engenharia", "Infraestrutura", "3.0", "Laboratórios precisam de atualização."],
            ["RES-003", "2026-07-11 09:15", "Administração", "Didática", "5.0", ""],
            ["RES-004", "2026-07-11 10:20", "Engenharia", "Inovação", "4.8", "Uso excelente de simulações em Python."],
        ]
        
        nome_arquivo = f"dados_brutos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        caminho_arquivo = os.path.join(os.getcwd(), nome_arquivo)
        
        try:
            with open(caminho_arquivo, mode='w', newline='', encoding='utf-8') as arquivo_csv:
                escritor = csv.writer(arquivo_csv, delimiter=';')
                escritor.writerows(dados_exportacao)
                
            page.snack_bar = ft.SnackBar(ft.Text(f"Arquivo CSV exportado com sucesso: {nome_arquivo}", color="green"))
            page.snack_bar.open = True
        except Exception as erro:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao exportar: {erro}", color="red"))
            page.snack_bar.open = True
            
        page.update()


    # === 2. COMPONENTES VISUAIS ===
    
    # --- Card 1: Controle do Ciclo de Avaliação ---
    status_ciclo = ft.Container(
        content=ft.Text("EM ANDAMENTO", color="white", size=12, weight="bold"),
        bgcolor="green600",
        # Solução à prova de falhas: um valor inteiro fixo para o preenchimento
        padding=8, 
        border_radius=15
    )

    card_controle_ciclo = ft.Container(
        bgcolor="white",
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
                                ft.Row([ft.Text("Semestre 2026.1", size=22, weight="bold", color="blue900"), status_ciclo])
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
        bgcolor="white",
        padding=25,
        border_radius=10,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color="black12"),
        content=ft.Column(
            expand=True,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text("Respostas Recentes (Raw Data)", size=18, weight="bold", color="black87"),
                        ft.ElevatedButton("Exportar CSV", icon=ft.Icons.DOWNLOAD, bgcolor="blue700", color="white", on_click=exportar_csv)
                    ]
                ),
                ft.Divider(color="grey200"),
                ft.Column(expand=True, scroll=ft.ScrollMode.AUTO, controls=[tabela_dados])
            ]
        )
    )

    # === 3. SIDEBAR PADRÃO ===
    estilo_botao_menu = ft.ButtonStyle(
        color={"":"white70", "hovered":"white"},
        bgcolor={"":"transparent", "hovered":"white10"},
        shape=ft.RoundedRectangleBorder(radius=8),
        padding=15,
        alignment=ft.Alignment(-1, 0) 
    )
    
    def sair(e):
        mudar_tela("/")

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
                ft.TextButton("Visão Geral", icon=ft.Icons.DASHBOARD, on_click=lambda _: mudar_tela("/dashboard"), style=estilo_botao_menu),
                ft.TextButton("Relatórios", icon=ft.Icons.PIE_CHART, on_click=lambda _: mudar_tela("/relatorios"), style=estilo_botao_menu),
                ft.TextButton("Cursos", icon=ft.Icons.BOOK, on_click=lambda _: mudar_tela("/cursos"), style=estilo_botao_menu),
                ft.TextButton("Configurações", icon=ft.Icons.SETTINGS, on_click=lambda _: mudar_tela("/configuracoes"), style=estilo_botao_menu),
                
                ft.Container(expand=True), 
                
                # Botão de Logout
                ft.TextButton(
                    "Sair do Sistema", 
                    icon=ft.Icons.LOGOUT, 
                    style=estilo_botao_menu,
                    on_click=sair
                )
            ]
        )
    )

    # === 4. ÁREA DE CONTEÚDO PRINCIPAL ===
    area_conteudo = ft.Container(
        expand=True,
        padding=40,
        bgcolor="#F4F6F9",
        content=ft.Column(
            expand=True,
            spacing=20,
            controls=[
                ft.Column(
                    spacing=5,
                    controls=[
                        ft.Text("Gestão de Ciclos e Respostas", size=28, weight="bold", color="black87"),
                        ft.Text("Monitore campanhas ativas e extraia os dados brutos das avaliações.", size=16, color="black54"),
                    ]
                ),
                card_controle_ciclo,
                card_tabela_dados
            ]
        )
    )

    return ft.View(
        route="/avaliacoes",
        padding=0,
        bgcolor="white",
        controls=[
            ft.Row(
                expand=True,
                spacing=0,
                controls=[sidebar, area_conteudo]
            )
        ]
    )