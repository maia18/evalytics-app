import flet as ft
from typing import Callable
from components.layout.responsive.responsive import ResponsiveLayout
from components.core.constants.constants import (
    COR_PRIMARIA, 
    BORDA,
)
from components.core.theme.border_utils import criar_borda_uniforme
from models.relatorios.widgets.filtros_relatorios import criar_secao_filtros
from models.relatorios.widgets.tables.tabela_resultados import criar_tabela_resultados
from models.relatorios.views.resultados_view import TelaResultados
from utils.services.relatorio.relatorio_service import (
    listar_resultados_avaliacoes, 
    filtrar_resultados,
)
from models.avaliacoes.core.csv.export_csv import exportar_csv
from core.pdf.relatorios_pdf_utils import processar_exportacao_pdf

def ViewRelatorios(page: ft.Page, mudar_tela: Callable[[str], None]) -> ft.View:

    # ==================================================
    # LAYOUT
    # ==================================================
    
    layout = ResponsiveLayout(
        page,
        titulo_pagina="Relatórios e Exportações",
        subtitulo="Analise indicadores visuais e exporte resultados consolidados.",
        mudar_tela=mudar_tela,
    )
    borda_container = criar_borda_uniforme(layout.cores[BORDA])

    # ==================================================
    # ESTADO (DADOS)
    # ==================================================
    
    resultados_originais = listar_resultados_avaliacoes()
    resultados_filtrados = list(resultados_originais)

    semestre_atual = None
    eixo_atual = None

    dashboard_visual = TelaResultados(page)

    # ==================================================
    # CALLBACKS DE EXPORTAÇÃO
    # ==================================================
    
    def exportar_csv_atual(e=None) -> None:
        exportar_csv(page, resultados=list(resultados_filtrados))

    def exportar_pdf_atual(e=None) -> None:
        processar_exportacao_pdf(page, resultados_filtrados, semestre_atual) # Delega a lógica complexa para o serviço auxiliar
        
    # ==================================================
    # TABELA E FILTROS
    # ==================================================
    
    tabela_resultados = criar_tabela_resultados(
        page,
        layout,
        borda_container,
        exportar_csv_atual,
        exportar_pdf_atual,
    )

    def aplicar_filtros(semestre: str | None, eixo: int | None) -> None:
        nonlocal resultados_filtrados, semestre_atual, eixo_atual

        semestre_atual = semestre
        eixo_atual = eixo

        resultados_filtrados = filtrar_resultados(
            resultados_originais,
            semestre=semestre,
            eixo=eixo,
        )

        if hasattr(dashboard_visual, "atualizar"):
            dashboard_visual.atualizar(semestre, eixo)

        # Atualiza a tabela (assumindo que o controle na posição 2 é o paginador/tabela)
        if hasattr(tabela_resultados.content.controls[2], "atualizar"):
            tabela_resultados.content.controls[2].atualizar(semestre, eixo)

        page.update()

    secao_filtros = criar_secao_filtros(
        layout,
        borda_container,
        page,
        aplicar_filtros,
        exportar_csv_atual,
        exportar_pdf_atual,
    )

    # ==================================================
    # ABAS E NAVEGAÇÃO INTERNA
    # ==================================================
    
    conteudo_aba_dados = ft.Container(
        expand=True,
        padding=ft.Padding.only(top=20),
        content=ft.Column(
            expand=True,
            controls=[tabela_resultados],
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
    conteudo_abas = ft.TabBarView(
        expand=True,
        controls=[dashboard_visual, conteudo_aba_dados],
    )
    
    indice_aba_relatorios = getattr(page, "indice_aba_relatorios", 0)
    
    def alterar_aba(e):
        page.indice_aba_relatorios = e.control.selected_index

    abas = ft.Tabs(
        length=2,
        selected_index=indice_aba_relatorios,
        animation_duration=300,
        expand=True,
        on_change=alterar_aba,
        content=ft.Column(
            expand=True,
            controls=[barra_abas, conteudo_abas],
        ),
    )

    # ==================================================
    # FINALIZAÇÃO
    # ==================================================
    
    conteudo = ft.Column(
        expand=True,
        controls=[
            secao_filtros,
            ft.Container(height=10),
            abas,
        ],
    )

    layout.add_content(conteudo)
    return layout.criar_view("/relatorios")