import flet as ft 
from components.core.constants.constants import *
from components.layout.responsive.responsive import ResponsiveLayout
from models.avaliacoes.avaliacoes import criar_conteudo_avaliacoes
from models.dashboard.widgets.kpi_cards import criar_kpi_card
from models.dashboard.widgets.grafico_eixos import criar_grafico_eixos


def ViewDashboard(page: ft.Page, mudar_tela): 
    layout = ResponsiveLayout( 
        page, 
        titulo_pagina="Dashboard",
        subtitulo="Indicadores de avaliação institucional",
        mudar_tela=mudar_tela
    ) 

    # === Dados simulados (Mock data) ===
    dados_kpi = { 
        "avaliacoes_ativas": "4",
        "respostas_coletadas": "1.248",
        "professores_avaliados": "82",
        "participacao": "74%"
    } 
    
    medias_eixos = {1: 4.5, 2: 4.1, 3: 3.4}
    nomes_eixos = {1: "Didático", 2: "Docente", 3: "Infra."}
    cores_barras = [COR_PRIMARIA, "#34D399", "#F87171"]

    # === Montagem dos KPIs ===
    linha_kpis = ft.Row( 
        wrap=True,
        spacing=20,
        run_spacing=20,
        controls=[ 
            criar_kpi_card(layout, "Avaliações ativas", dados_kpi["avaliacoes_ativas"], ft.Icons.ASSIGNMENT_OUTLINED, COR_PRIMARIA),
            criar_kpi_card(layout, "Respostas coletadas", dados_kpi["respostas_coletadas"], ft.Icons.TRENDING_UP, COR_PRIMARIA),
            criar_kpi_card(layout, "Professores avaliados", dados_kpi["professores_avaliados"], ft.Icons.SCHOOL_OUTLINED, COR_PRIMARIA),
            criar_kpi_card(layout, "Participação", dados_kpi["participacao"], ft.Icons.PEOPLE_OUTLINE, COR_PRIMARIA)
        ] 
    ) 

    # === Montagem do Gráfico ===
    area_graficos = criar_grafico_eixos(layout, medias_eixos, nomes_eixos, cores_barras)

    # === Conteúdo de cada aba ===
    # IMPORTANTE: expand=True fica no Container (dá o limite de altura vindo do TabBarView),
    # e scroll=AUTO fica isolado na Column interna, SEM expand=True nela mesma.
    # Isso evita o bug do Flet de espaço em branco + scroll fantasma quando
    # expand e scroll são combinados na mesma Column (github.com/flet-dev/flet/issues/6087).
    conteudo_dashboard_executivo = ft.Container(
        expand=True, # Ancora o container no TabBarView, dando altura limitada
        content=ft.Column(
            spacing=16, # Reduzido de 25 para 16: menos espaço entre KPIs e gráfico
            scroll=ft.ScrollMode.AUTO, # Rola somente se o conteúdo real ultrapassar o espaço disponível
            controls=[ft.Container(height=8), linha_kpis, area_graficos] # Spacer do topo reduzido de 20 para 8
        )
    )
    
    # === Abas (Mantendo as restrições corretas) ===
    barra_abas = ft.TabBar(
        tabs=[
            ft.Tab(label="Dashboard", icon=ft.Icons.GRID_VIEW_ROUNDED),
            ft.Tab(label="Gestão de Ciclos e Respostas", icon=ft.Icons.TABLE_ROWS_ROUNDED),
        ],
        label_color=COR_PRIMARIA,
        unselected_label_color="grey600",
        indicator_color=COR_PRIMARIA,
        divider_color=layout.cores[BORDA],
    )

    conteudo_abas = ft.TabBarView(
        expand=True,
        controls=[
            conteudo_dashboard_executivo,
            criar_conteudo_avaliacoes(layout, mudar_tela, page)
        ],
    )

    abas = ft.Tabs(
        length=2,
        expand=True,
        content=ft.Column(
            expand=True,
            controls=[barra_abas, conteudo_abas],
        ),
    )

    # === Layout final da página ===
    conteudo = ft.Column( 
        expand=True, 
        controls=[abas] 
    ) 

    layout.add_content(conteudo)
    return layout.criar_view("/dashboard")