import flet as ft
from components.responsive_layout import ResponsiveLayout

def ViewInicio(page: ft.Page, mudar_tela):
    """Página inicial do Evalytics com layout responsivo"""
    
    # Criar o layout responsivo
    layout = ResponsiveLayout(
        page, 
        "Início", 
        "Bem-vindo ao Evalytics", 
        mudar_tela=mudar_tela
    )    
    
    
    # Função auxiliar para criar cards clicáveis
    def criar_card(titulo, descricao, icone, rota):
        return ft.Container(
            width=300,
            bgcolor=layout.COR_CARD,
            padding=20,
            border_radius=12,
            border=ft.Border(
                left=ft.BorderSide(width=1, color=layout.COR_BORDA),
                top=ft.BorderSide(width=1, color=layout.COR_BORDA),
                right=ft.BorderSide(width=1, color=layout.COR_BORDA),
                bottom=ft.BorderSide(width=1, color=layout.COR_BORDA),
            ),
            ink=True,
            on_click=lambda e: mudar_tela(rota),
            content=ft.Column([
                ft.Icon(icone, color=layout.COR_PRIMARIA, size=30),
                ft.Text(titulo, weight="bold", color=layout.COR_TEXTO_PRINCIPAL),
                ft.Text(descricao, size=12, color="grey")
            ])
        )

    # Conteúdo principal
    conteudo = ft.Column(
        expand=True,
        controls=[
            ft.Container(
                bgcolor=layout.COR_CARD,
                padding=25,
                border_radius=12,
                border=ft.Border(
                    left=ft.BorderSide(1, layout.COR_BORDA),
                    top=ft.BorderSide(1, layout.COR_BORDA),
                    right=ft.BorderSide(1, layout.COR_BORDA),
                    bottom=ft.BorderSide(1, layout.COR_BORDA)
                ),
                content=ft.Column([
                    ft.Text(
                        "Sistema de Avaliação Institucional", 
                        weight="bold", 
                        size=20,
                        color=layout.COR_TEXTO_PRINCIPAL
                    ),
                    ft.ElevatedButton(
                        "Iniciar nova avaliação", 
                        bgcolor=layout.COR_PRIMARIA, 
                        color="white",
                        on_click=lambda e: mudar_tela("/formulario")
                    )
                ])
            ),
            ft.Container(height=20),
            ft.Row(
                wrap=True,
                spacing=20,
                run_spacing=20,
                controls=[
                    criar_card("Nova Avaliação", "Criar um novo instrumento.", ft.Icons.ADD, "/formulario"),
                    criar_card("Dashboard", "Visão geral dos indicadores.", ft.Icons.GRID_VIEW, "/dashboard"),
                    criar_card("Cursos", "Consultar e organizar cursos.", ft.Icons.MENU_BOOK, "/cursos"),
                    criar_card("Relatórios", "Gerar relatórios.", ft.Icons.PIE_CHART, "/relatorios"),
                ]
            )
        ]
    )
    
    # Adicionar conteúdo ao layout
    layout.add_content(conteudo)
    
    # Retornar a view
    return layout.criar_view("/inicio")