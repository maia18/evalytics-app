import flet as ft
from components.layout.responsive.responsive import ResponsiveLayout
from components.core.constants.constants import *

# Importa os subcomponentes isolados (Tabela e Filtros)
from models.relatorios.widgets.filtros_relatorios import criar_secao_filtros
from models.relatorios.widgets.tabela_resultados import criar_tabela_resultados

# Importa o seu Dashboard Executivo recém-criado que está na pasta views
from models.relatorios.views.resultados_view import TelaResultados

def ViewRelatorios(page: ft.Page, mudar_tela):
    """
    Renderiza a tela principal de 'Relatórios e Exportações'.
    Utiliza um sistema de Abas (Tabs) para organizar a exibição entre o 
    Dashboard Gráfico e a Tabela de Dados Brutos.
    """
    
    layout = ResponsiveLayout(
        page,
        titulo_pagina="Relatórios e Exportações",
        subtitulo="Analise indicadores visuais e exporte resultados consolidados.",
        mudar_tela=mudar_tela
    )

    borda_container = ft.Border(
        top=ft.BorderSide(1, layout.cores[BORDA]),
        bottom=ft.BorderSide(1, layout.cores[BORDA]),
        left=ft.BorderSide(1, layout.cores[BORDA]),
        right=ft.BorderSide(1, layout.cores[BORDA]),
    )

    # === Instanciação dos Componentes ===
    secao_filtros = criar_secao_filtros(layout, borda_container, page)
    tabela_resultados = criar_tabela_resultados(page, layout, borda_container)
    
    # Instancia a View do Dashboard Executivo
    dashboard_visual = TelaResultados(page)

    # === Montagem do Sistema de Abas (Tabs) ===
    abas = ft.Tabs(
        selected_index=0, # Inicia mostrando o Dashboard por padrão
        animation_duration=300, # Transição suave entre as abas
        expand=True,
        tabs=[
            # Aba 1: Dashboard Executivo
            ft.Tab(
                text="Dashboard Executivo",
                icon=ft.Icons.DASHBOARD,
                content=dashboard_visual # Injeta a sua view visual aqui
            ),
            
            # Aba 2: Dados e Exportações (Filtros + Tabela)
            ft.Tab(
                text="Dados Brutos e Exportação",
                icon=ft.Icons.TABLE_CHART,
                content=ft.Container(
                    padding=ft.padding.only(top=20), # Respiro antes de começar o conteúdo
                    content=ft.Column(
                        expand=True,
                        controls=[
                            secao_filtros,
                            ft.Divider(height=20, color="transparent"),
                            tabela_resultados
                        ]
                    )
                )
            ),
        ]
    )

    # === Montagem do Layout Principal ===
    conteudo = ft.Column(
        expand=True,
        controls=[
            # Todo aquele cabeçalho de texto foi removido daqui pois o ResponsiveLayout
            # já cuida do título da página na Topbar. Inserimos direto as abas!
            abas
        ]
    )

    layout.add_content(conteudo)
    return layout.criar_view("/relatorios")