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
from models.avaliacoes.core.csv.export_csv import exportar_csv
from models.relatorios.core.pdf.relatorios_pdf_utils import (
    NOMES_EIXOS as NOMES_EIXOS_PDF,
    processar_exportacao_pdf,
)
from database.services.cursos.firestore_courses import obter_cursos_db
from utils.services.cursos.curso_utils import (
    chave_curso,
    listar_nomes_cursos_filtraveis,
)
from utils.services.relatorio.relatorio_service import listar_resultados_avaliacoes 
from utils.services.relatorio.relatorio_utils import filtrar_resultados, obter_semestre

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
    curso_atual = None
    eixo_atual = None

    dashboard_visual = TelaResultados(page)

    # ==================================================
    # CALLBACKS DE EXPORTAÇÃO
    # ==================================================
    
    def exportar_csv_atual(e=None) -> None:
        exportar_csv(page, resultados=list(resultados_filtrados))

    def exportar_pdf_atual(e=None) -> None:
        if not resultados_originais:
            processar_exportacao_pdf(page, [], None)
            return

        cursos_disponiveis = listar_nomes_cursos_filtraveis(
            resultados_originais,
            obter_cursos_db(),
        )
        semestres_disponiveis = sorted(
            {
                resultado.get("semestre")
                or obter_semestre(resultado.get("data_avaliacao"))
                for resultado in resultados_originais
                if resultado.get("semestre")
                or obter_semestre(resultado.get("data_avaliacao"))
            },
            reverse=True,
        )

        dropdown_curso = ft.Dropdown(
            label="Curso",
            value="TODOS",
            options=[
                ft.dropdown.Option(key="TODOS", text="Todos os cursos"),
                *[
                    ft.dropdown.Option(key=curso, text=curso)
                    for curso in cursos_disponiveis
                ],
            ],
            autofocus=True,
        )
        dropdown_semestre_pdf = ft.Dropdown(
            label="Semestre",
            value="TODOS",
            options=[
                ft.dropdown.Option(key="TODOS", text="Todos os semestres"),
                *[
                    ft.dropdown.Option(key=semestre, text=semestre)
                    for semestre in semestres_disponiveis
                ],
            ],
        )
        dropdown_eixo_pdf = ft.Dropdown(
            label="Eixo avaliativo",
            value="TODOS",
            options=[
                ft.dropdown.Option(key="TODOS", text="Todos os eixos"),
                *[
                    ft.dropdown.Option(key=str(eixo_id), text=nome)
                    for eixo_id, nome in NOMES_EIXOS_PDF.items()
                ],
            ],
        )

        def fechar_modal() -> None:
            modal.open = False
            page.update()

        def gerar_pdf_selecionado(e=None) -> None:
            semestre = (
                dropdown_semestre_pdf.value
                if dropdown_semestre_pdf.value != "TODOS"
                else None
            )
            eixo = (
                int(dropdown_eixo_pdf.value)
                if dropdown_eixo_pdf.value != "TODOS"
                else None
            )
            curso = dropdown_curso.value

            resultados_pdf = filtrar_resultados(
                resultados_originais,
                semestre=semestre,
                eixo=eixo,
            )
            if curso != "TODOS":
                resultados_pdf = [
                    resultado
                    for resultado in resultados_pdf
                    if chave_curso(
                        resultado.get("curso_nome", resultado.get("curso", ""))
                    ) == chave_curso(curso)
                ]

            fechar_modal()
            processar_exportacao_pdf(
                page,
                resultados_pdf,
                semestre or "Todos",
                eixo,
            )

        modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Gerar relatório PDF", size=20, weight="bold"),
            content=ft.Column(
                width=420,
                height=230,
                spacing=12,
                controls=[
                    ft.Text("Escolha os dados que deseja incluir no relatório."),
                    dropdown_curso,
                    dropdown_semestre_pdf,
                    dropdown_eixo_pdf,
                ],
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: fechar_modal()),
                ft.ElevatedButton(
                    "Gerar PDF",
                    icon=ft.Icons.PICTURE_AS_PDF,
                    bgcolor=ft.Colors.RED_700,
                    color=ft.Colors.WHITE,
                    on_click=gerar_pdf_selecionado,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        if modal not in page.overlay:
            page.overlay.append(modal)
        modal.open = True
        page.update()
        
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

    def aplicar_filtros(
        semestre: str | None,
        curso_nome: str | None,
        eixo: int | None,
    ) -> None:
        nonlocal resultados_filtrados, semestre_atual, curso_atual, eixo_atual

        semestre_atual = semestre
        curso_atual = curso_nome
        eixo_atual = eixo

        resultados_filtrados = filtrar_resultados(
            resultados_originais,
            semestre=semestre,
            eixo=eixo,
            curso_nome=curso_nome,
        )

        if hasattr(dashboard_visual, "atualizar"):
            dashboard_visual.atualizar(semestre, curso_nome, eixo)

        # Atualiza a tabela (assumindo que o controle na posição 2 é o paginador/tabela)
        if hasattr(tabela_resultados.content.controls[2], "atualizar"):
            tabela_resultados.content.controls[2].atualizar(
                semestre,
                curso_nome,
                eixo,
            )

        page.update()

    secao_filtros = criar_secao_filtros(
        layout,
        borda_container,
        page,
        aplicar_filtros,
        exportar_csv_atual,
        exportar_pdf_atual,
        resultados=resultados_originais,
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
