import flet as ft
from components.layout.responsive.responsive import ResponsiveLayout

from models.dashboard.widgets.kpi_cards import criar_kpi_card
from models.dashboard.widgets.grafico_eixos import criar_grafico_eixos

from components.core.constants import *

def ViewDashboard(page: ft.Page, mudar_tela):
    layout = ResponsiveLayout(
        page,
        titulo_pagina="Dashboard",
        subtitulo="Indicadores de avaliação institucional",
        mudar_tela=mudar_tela
    )

    # Dados simulados
    dados_kpi = {
        "avaliacoes_ativas": "4",
        "respostas_coletadas": "1.248",
        "professores_avaliados": "82",
        "participacao": "74%"
    }
    medias_eixos = {1: 4.5, 2: 4.1, 3: 3.4}
    nomes_eixos = {1: "Didático", 2: "Docente", 3: "Infra."}
    cores_barras = [PRIMARIA, "#34D399", "#F87171"]

    # KPIs
    linha_kpis = ft.Row(
        wrap=True,
        spacing=20,
        run_spacing=20,
        controls=[
            criar_kpi_card(layout, "Avaliações ativas", dados_kpi["avaliacoes_ativas"], ft.Icons.ASSIGNMENT_OUTLINED, PRIMARIA),
            criar_kpi_card(layout, "Respostas coletadas", dados_kpi["respostas_coletadas"], ft.Icons.TRENDING_UP, PRIMARIA),
            criar_kpi_card(layout, "Professores avaliados", dados_kpi["professores_avaliados"], ft.Icons.SCHOOL_OUTLINED, PRIMARIA),
            criar_kpi_card(layout, "Participação", dados_kpi["participacao"], ft.Icons.PEOPLE_OUTLINE, PRIMARIA)
        ]
    )

    # Gráfico
    area_graficos = criar_grafico_eixos(layout, medias_eixos, nomes_eixos, cores_barras)

    # Layout final
    conteudo = ft.Column(
        expand=True,
        spacing=25,
        scroll=ft.ScrollMode.AUTO,
        controls=[linha_kpis, area_graficos]
    )

    layout.add_content(conteudo)
    return layout.criar_view("/dashboard")