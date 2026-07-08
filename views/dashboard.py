import flet as ft
# Importamos a nossa nova tela
from views.professores_view import TelaProfessores

def ViewDashboard(page: ft.Page, mudar_tela):
    
    # Este container é a área em branco onde as telas vão se alternar
    area_conteudo = ft.Container(padding=40, expand=True)

    # A tela de Início (Index 0)
    tela_inicio = ft.Column(
        controls=[
            ft.Text("Visão Geral do Sistema", size=30, weight=ft.FontWeight.BOLD),
            ft.Text("Selecione um módulo no menu lateral para começar.", size=16),
            ft.Divider(height=40, color=ft.Colors.TRANSPARENT),
            ft.ElevatedButton("Sair do Sistema", on_click=lambda _: mudar_tela("/"), color="red")
        ]
    )

    # Define a tela inicial como padrão ao abrir o Dashboard
    area_conteudo.content = tela_inicio

    # Função que troca o conteúdo dependendo de onde o usuário clica no menu
    def alterar_aba(e):
        index = e.control.selected_index
        
        if index == 0:
            area_conteudo.content = tela_inicio
        elif index == 1:
            area_conteudo.content = TelaProfessores(page)
        else:
            # Para os menus que ainda não criamos
            area_conteudo.content = ft.Text(f"Módulo em construção...", size=20)
        
        page.update()

    menu_lateral = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(icon=ft.Icons.DASHBOARD, label="Início"), # Index 0
            ft.NavigationRailDestination(icon=ft.Icons.PEOPLE, label="Professores"), # Index 1
            ft.NavigationRailDestination(icon=ft.Icons.MENU_BOOK, label="Disciplinas"),
            ft.NavigationRailDestination(icon=ft.Icons.FACT_CHECK, label="Indicadores"),
            ft.NavigationRailDestination(icon=ft.Icons.BAR_CHART, label="Relatórios"),
        ],
        on_change=alterar_aba
    )

    layout_dashboard = ft.Row(
        controls=[
            menu_lateral,
            ft.VerticalDivider(width=1),
            area_conteudo
        ],
        expand=True
    )

    return ft.View(
        route="/dashboard",
        appbar=ft.AppBar(title=ft.Text("Painel Administrativo Evalytics", color="white"), bgcolor="blue700"),
        controls=[layout_dashboard]
    )