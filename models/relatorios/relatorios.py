import flet as ft
from components.layout.responsive.responsive import ResponsiveLayout
from models.relatorios.widgets.filtros_relatorios import criar_secao_filtros
from models.relatorios.widgets.tabela_resultados import criar_tabela_resultados

def ViewRelatorios(page: ft.Page, mudar_tela):
    layout = ResponsiveLayout(
        page,
        titulo_pagina="Relatórios e Exportações",
        subtitulo="Gere visualizações dinâmicas e exporte resultados.",
        mudar_tela=mudar_tela
    )

    borda_container = ft.Border(
        top=ft.BorderSide(1, layout.cores["BORDA"]),
        bottom=ft.BorderSide(1, layout.cores["BORDA"]),
        left=ft.BorderSide(1, layout.cores["BORDA"]),
        right=ft.BorderSide(1, layout.cores["BORDA"]),
    )

    secao_filtros = criar_secao_filtros(layout, borda_container)
    tabela_resultados = criar_tabela_resultados(page, layout, borda_container)

    conteudo = ft.Column(
        expand=True,
        controls=[
            ft.Text("Relatórios e Exportações", size=28, weight="bold", color=layout.cores["TEXTO_PRINCIPAL"]),
            ft.Text("Gere visualizações dinâmicas, analise os critérios e exporte os resultados.", size=16, color="grey"),
            ft.Divider(height=30, color="transparent"),
            secao_filtros,
            ft.Divider(height=20, color="transparent"),
            tabela_resultados
        ]
    )

    layout.add_content(conteudo)
    return layout.criar_view("/relatorios")