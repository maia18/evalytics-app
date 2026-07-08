import flet as ft

def ViewDashboard(page: ft.Page, mudar_tela):
    menu_lateral = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(icon=ft.Icons.DASHBOARD, label="Início"),
            ft.NavigationRailDestination(icon=ft.Icons.PEOPLE, label="Professores"),
            ft.NavigationRailDestination(icon=ft.Icons.MENU_BOOK, label="Disciplinas"),
            ft.NavigationRailDestination(icon=ft.Icons.FACT_CHECK, label="Indicadores"),
            ft.NavigationRailDestination(icon=ft.Icons.BAR_CHART, label="Relatórios"),
        ],
        on_change=lambda e: print(f"Clicou no menu: {e.control.selected_index}")
    )

    area_conteudo = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Visão Geral do Sistema", size=30, weight=ft.FontWeight.BOLD),
                ft.Text("Selecione um módulo no menu lateral para começar.", size=16),
                ft.Divider(height=40, color=ft.Colors.TRANSPARENT),
                ft.ElevatedButton("Sair do Sistema", on_click=lambda _: mudar_tela("/"), color="red")
            ]
        ),
        padding=40,
        expand=True
    )

    layout_dashboard = ft.Row(
        controls=[
            menu_lateral,
            ft.VerticalDivider(width=1),
            area_conteudo
        ],
        expand=True
    )

    # Retorna a View montada
    return ft.View(
        route="/dashboard",
        appbar=ft.AppBar(title=ft.Text("Painel Administrativo Evalytics", color="white"), bgcolor="blue700"),
        controls=[layout_dashboard]
    )