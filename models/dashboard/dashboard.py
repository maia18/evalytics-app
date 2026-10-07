from typing import Callable

import flet as ft

from components.core.constants.constants import (
    COR_PRIMARIA,
    BORDA,
    TEXTO_PRINCIPAL,
    TEXTO_SECUNDARIO,
)

from components.layout.responsive.responsive import ResponsiveLayout

from models.avaliacoes.avaliacoes import (
    criar_conteudo_avaliacoes,
)

from models.dashboard.widgets.kpi_cards import (
    criar_kpi_card,
)

from models.dashboard.widgets.grafico_eixos import (
    criar_grafico_eixos,
)

from database.services.firestore_dashboard import (
    obter_dados_dashboard,
)


# ==========================================================
# CORES DAS BARRAS
# ==========================================================

CORES_BARRAS_GRAFICO_EIXOS = [
    COR_PRIMARIA,
    "#34D399",
    "#F87171",
]


# ==========================================================
# NOMES DOS EIXOS
# ==========================================================

NOMES_EIXOS = {
    1: "Organização Didático-Pedagógica",
    2: "Corpo Docente e Tutorial",
    3: "Infraestrutura",
}


def ViewDashboard(
    page: ft.Page,
    mudar_tela: Callable[[str], None],
) -> ft.View:
    """
    Constrói a página principal do Dashboard.

    A primeira aba apresenta uma visão consolidada
    dos dados reais das avaliações.

    A segunda aba apresenta o acompanhamento
    das avaliações registradas.
    """

    # ==========================================================
    # LAYOUT
    # ==========================================================

    layout = ResponsiveLayout(
        page,
        titulo_pagina="Indicadores de Avaliação",
        subtitulo=(
            "Acompanhe os resultados e a evolução "
            "das avaliações institucionais."
        ),
        mudar_tela=mudar_tela,
    )

    # ==========================================================
    # DADOS REAIS
    # ==========================================================

    dados_dashboard = obter_dados_dashboard()

    quantidade_avaliacoes = dados_dashboard[
        "avaliacoes"
    ]

    quantidade_respostas = dados_dashboard[
        "respostas"
    ]

    quantidade_cursos = dados_dashboard[
        "cursos"
    ]

    media_geral = dados_dashboard[
        "media_geral"
    ]

    medias_eixos = dados_dashboard[
        "medias_eixos"
    ]

    # ==========================================================
    # KPIs
    # ==========================================================

    linha_kpis = ft.Row(
        wrap=True,
        spacing=20,
        run_spacing=20,
        controls=[
            criar_kpi_card(
                layout,
                "Avaliações realizadas",
                str(quantidade_avaliacoes),
                ft.Icons.ASSIGNMENT_OUTLINED,
                COR_PRIMARIA,
            ),

            criar_kpi_card(
                layout,
                "Respostas registradas",
                f"{quantidade_respostas:,}".replace(
                    ",",
                    ".",
                ),
                ft.Icons.TRENDING_UP,
                COR_PRIMARIA,
            ),

            criar_kpi_card(
                layout,
                "Cursos avaliados",
                str(quantidade_cursos),
                ft.Icons.SCHOOL_OUTLINED,
                COR_PRIMARIA,
            ),

            criar_kpi_card(
                layout,
                "Média geral",
                (
                    f"{media_geral:.1f}"
                    if quantidade_respostas
                    else "—"
                ),
                ft.Icons.STAR_OUTLINE,
                COR_PRIMARIA,
            ),
        ],
    )

    # ==========================================================
    # GRÁFICO POR EIXO
    # ==========================================================

    area_graficos = criar_grafico_eixos(
        layout,
        medias_eixos,
        NOMES_EIXOS,
        CORES_BARRAS_GRAFICO_EIXOS,
    )
    
    indice_aba_atual = getattr(page, "_dashboard_aba_atual", 0)

    # ==========================================================
    # CONTEÚDO DA PRIMEIRA ABA
    # ==========================================================

    conteudo_dashboard_executivo = ft.Container(
        expand=True,
        content=ft.Column(
            spacing=16,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Container(height=8),
                linha_kpis,
                area_graficos,
            ],
        ),
    )

    # ==========================================================
    # ABAS
    # ==========================================================

    barra_abas = ft.TabBar(
        tabs=[
            ft.Tab(
                label="Visão Geral",
                icon=ft.Icons.GRID_VIEW_ROUNDED,
            ),
            ft.Tab(
                label="Acompanhamento das Avaliações",
                icon=ft.Icons.TABLE_ROWS_ROUNDED,
            ),
        ],
        label_color=COR_PRIMARIA,
        unselected_label_color=(
            layout.cores[TEXTO_SECUNDARIO]
        ),
        indicator_color=COR_PRIMARIA,
        divider_color=layout.cores[BORDA],
    )

    # ==========================================================
    # CONTEÚDO DAS ABAS
    # ==========================================================

    conteudo_abas = ft.TabBarView(
        expand=True,
        controls=[
            conteudo_dashboard_executivo,

            criar_conteudo_avaliacoes(
                layout,
                mudar_tela,
                page,
            ),
        ],
    )

    abas = ft.Tabs(
        length=2,
        selected_index=indice_aba_atual,
        on_change=lambda e: setattr(
            page,
            "_dashboard_aba_atual",
            e.control.selected_index,
        ),
        expand=True,
        content=ft.Column(
            expand=True,
            controls=[
                barra_abas,
                conteudo_abas,
            ],
        ),
    )

    conteudo = ft.Column(
        expand=True,
        controls=[
            abas,
        ],
    )

    # ==========================================================
    # FINALIZAÇÃO
    # ==========================================================

    layout.add_content(conteudo)

    return layout.criar_view("/dashboard")