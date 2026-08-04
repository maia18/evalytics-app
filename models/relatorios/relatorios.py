from typing import Callable

import flet as ft

from components.layout.responsive.responsive import ResponsiveLayout
from components.core.constants.constants import COR_PRIMARIA, BORDA
from components.core.theme.border_utils import criar_borda_uniforme

from models.relatorios.widgets.filtros_relatorios import criar_secao_filtros
from models.relatorios.widgets.tabela_resultados import criar_tabela_resultados
from models.relatorios.views.resultados_view import TelaResultados


def ViewRelatorios(page: ft.Page, mudar_tela: Callable[[str], None]) -> ft.View:
    """Renderiza a tela de 'Relatórios e Exportações', com abas para Dashboard Executivo e Dados Brutos."""
    layout = ResponsiveLayout(
        page,
        titulo_pagina="Relatórios e Exportações",
        subtitulo="Analise indicadores visuais e exporte resultados consolidados.",
        mudar_tela=mudar_tela,
    )

    borda_container = criar_borda_uniforme(layout.cores[BORDA])

    secao_filtros = criar_secao_filtros(layout, borda_container, page)
    tabela_resultados = criar_tabela_resultados(page, layout, borda_container)
    dashboard_visual = TelaResultados(page)

    conteudo_aba_dados = ft.Container(
        expand=True,
        padding=ft.Padding.only(top=20),
        content=ft.Column(
            expand=True,
            controls=[
                secao_filtros,
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                tabela_resultados,
            ],
        ),
    )

    barra_abas = ft.TabBar(
        tabs=[
            ft.Tab(label="Dashboard Executivo", icon=ft.Icons.DASHBOARD),
            ft.Tab(label="Dados Brutos e Exportação", icon=ft.Icons.TABLE_CHART),
        ],
        label_color=COR_PRIMARIA,
        unselected_label_color=ft.Colors.GREY_600,
        indicator_color=COR_PRIMARIA,
        divider_color=layout.cores[BORDA],
    )

    conteudo_abas = ft.TabBarView(expand=True, controls=[dashboard_visual, conteudo_aba_dados])

    abas = ft.Tabs(
        length=2,
        selected_index=0,
        animation_duration=300,
        expand=True,
        content=ft.Column(expand=True, controls=[barra_abas, conteudo_abas]),
    )

    conteudo = ft.Column(expand=True, controls=[abas])

    layout.add_content(conteudo)
    return layout.criar_view("/relatorios")