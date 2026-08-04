from typing import Callable
import flet as ft

from components.core.constants.constants import COR_PRIMARIA, BORDA
from components.layout.responsive.responsive import ResponsiveLayout

from models.avaliacoes.avaliacoes import criar_conteudo_avaliacoes
from models.dashboard.widgets.kpi_cards import criar_kpi_card
from models.dashboard.widgets.grafico_eixos import criar_grafico_eixos
from models.dashboard.layout.card_grafico_desempenho import criar_card_grafico_desempenho

# Cores das barras do gráfico de eixos. 
# A segunda e a terceira cores são decorativas (verde/vermelho de gráfico) e não fazem parte da paleta dinâmica de tema claro/escuro.
CORES_BARRAS_GRAFICO_EIXOS = [COR_PRIMARIA, "#34D399", "#F87171"]


def ViewDashboard(page: ft.Page, mudar_tela: Callable[[str], None]) -> ft.View:
    """Constrói a página principal do Dashboard com navegação por abas."""
    layout = ResponsiveLayout(
        page, titulo_pagina="Dashboard", subtitulo="Indicadores de avaliação institucional", mudar_tela=mudar_tela,
    )

    # === Dados simulados (Mock data) ===
    # Estes dados dos KPIs e do gráfico de eixos poderão ser substituídos por funções do Firestore futuramente.
    dados_kpi = {
        "avaliacoes_ativas": "4",
        "respostas_coletadas": "1.248",
        "professores_avaliados": "82",
        "participacao": "74%",
    }

    medias_eixos = {1: 4.5, 2: 4.1, 3: 3.4}
    nomes_eixos = {1: "Didático", 2: "Docente", 3: "Infra."}

    # === Montagem da linha de KPIs ===
    linha_kpis = ft.Row(
        wrap=True,  # Responsividade: cards descem para a próxima linha automaticamente se a tela encolher
        spacing=20, run_spacing=20,
        controls=[
            criar_kpi_card(layout, "Avaliações ativas", dados_kpi["avaliacoes_ativas"], ft.Icons.ASSIGNMENT_OUTLINED, COR_PRIMARIA),
            criar_kpi_card(layout, "Respostas coletadas", dados_kpi["respostas_coletadas"], ft.Icons.TRENDING_UP, COR_PRIMARIA),
            criar_kpi_card(layout, "Professores avaliados", dados_kpi["professores_avaliados"], ft.Icons.SCHOOL_OUTLINED, COR_PRIMARIA),
            criar_kpi_card(layout, "Participação", dados_kpi["participacao"], ft.Icons.PEOPLE_OUTLINE, COR_PRIMARIA),
        ],
    )

    area_graficos = criar_grafico_eixos(layout, medias_eixos, nomes_eixos, CORES_BARRAS_GRAFICO_EIXOS)
    card_desempenho = criar_card_grafico_desempenho(layout)

    # IMPORTANTE ARQUITETURAL: expand=True fica no Container (dando o limite de altura vindo do TabBarView).
    # O scroll=AUTO fica isolado na Column interna, sem expand=True nela mesma.
    # Isso evita o bug do Flet de espaço em branco e scroll fantasma quando combinados na mesma Column.
    conteudo_dashboard_executivo = ft.Container(
        expand=True,
        content=ft.Column(
            spacing=16, scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Container(height=8),
                linha_kpis,
                area_graficos,
                card_desempenho,
            ],
        ),
    )

    # === Configuração das Abas (Tabs) ===
    barra_abas = ft.TabBar(
        tabs=[
            ft.Tab(label="Dashboard", icon=ft.Icons.GRID_VIEW_ROUNDED),
            ft.Tab(label="Gestão de Ciclos e Respostas", icon=ft.Icons.TABLE_ROWS_ROUNDED),
        ],
        label_color=COR_PRIMARIA,
        unselected_label_color=ft.Colors.GREY_600,
        indicator_color=COR_PRIMARIA,
        divider_color=layout.cores[BORDA],
    )

    conteudo_abas = ft.TabBarView(
        expand=True,
        controls=[
            conteudo_dashboard_executivo,
            criar_conteudo_avaliacoes(layout, mudar_tela, page),  # Reaproveita a tela inteira de Avaliações construída anteriormente
        ],
    )

    abas = ft.Tabs(length=2, expand=True, content=ft.Column(expand=True, controls=[barra_abas, conteudo_abas]))
    conteudo = ft.Column(expand=True, controls=[abas])

    layout.add_content(conteudo)
    return layout.criar_view("/dashboard")