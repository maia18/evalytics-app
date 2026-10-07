from typing import Callable

import flet as ft

from components.layout.responsive.responsive import ResponsiveLayout
from components.core.constants.constants import COR_PRIMARIA, BORDA
from components.core.theme.border_utils import criar_borda_uniforme

from models.relatorios.widgets.filtros_relatorios import criar_secao_filtros
from models.relatorios.widgets.tabela_resultados import criar_tabela_resultados
from models.relatorios.views.resultados_view import TelaResultados

from utils.services.relatorio_service import (
    listar_resultados_avaliacoes,
    filtrar_resultados,
)

from models.avaliacoes.core.export_csv import exportar_csv
from models.relatorios.core.export_pdf import normalizar_nome_curso, gerar_pdf_completo


NOMES_EIXOS = {
    1: "Organização Didático-Pedagógica",
    2: "Corpo Docente e Tutorial",
    3: "Infraestrutura",
}


def ViewRelatorios(
    page: ft.Page,
    mudar_tela: Callable[[str], None],
) -> ft.View:

    # ==================================================
    # LAYOUT
    # ==================================================

    layout = ResponsiveLayout(
        page,
        titulo_pagina="Relatórios e Exportações",
        subtitulo=(
            "Analise indicadores visuais e "
            "exporte resultados consolidados."
        ),
        mudar_tela=mudar_tela,
    )

    borda_container = criar_borda_uniforme(
        layout.cores[BORDA]
    )

    # ==================================================
    # DADOS
    # ==================================================

    resultados_originais = listar_resultados_avaliacoes()

    resultados_filtrados = list(
        resultados_originais
    )

    semestre_atual = None
    eixo_atual = None

    # ==================================================
    # DASHBOARD
    # ==================================================

    dashboard_visual = TelaResultados(
        page
    )

    # ==================================================
    # EXPORTAR CSV
    # ==================================================

    def exportar_csv_atual(e=None) -> None:
        exportar_csv(
            page,
            resultados=list(
                resultados_filtrados
            ),
        )

    # ==================================================
    # CALCULAR MÉDIAS PARA PDF
    # ==================================================

    def calcular_medias_pdf() -> dict[int, float | None]:

        acumuladores = {
            1: [],
            2: [],
            3: [],
        }

        for resultado in resultados_filtrados:

            eixos = resultado.get(
                "eixos",
                {},
            )

            if not isinstance(
                eixos,
                dict,
            ):
                continue

            for eixo_id in (
                1,
                2,
                3,
            ):

                valor = eixos.get(
                    eixo_id
                )

                if valor is None:
                    continue

                try:
                    valor = float(valor)

                except (
                    TypeError,
                    ValueError,
                ):
                    continue

                if valor <= 0:
                    continue

                acumuladores[
                    eixo_id
                ].append(valor)

        medias = {}

        for eixo_id, notas in acumuladores.items():

            if notas:
                medias[eixo_id] = (
                    sum(notas)
                    / len(notas)
                )

            else:
                medias[eixo_id] = None

        return medias

    # ==================================================
    # EXPORTAR PDF
    # ==================================================

    def exportar_pdf_atual(e=None) -> None:

        # --------------------------------------------------
        # VALIDAÇÃO
        # --------------------------------------------------

        if not resultados_filtrados:

            from models.avaliacoes.core.feedback import (
                mostrar_feedback,
            )

            mostrar_feedback(
                page,
                "Não existem dados para gerar o PDF.",
                sucesso=False,
            )

            return

        # --------------------------------------------------
        # MÉDIAS
        # --------------------------------------------------

        medias = calcular_medias_pdf()

        medias_validas = {
            eixo_id: media
            for eixo_id, media in medias.items()
            if media is not None
        }

        if not medias_validas:

            from models.avaliacoes.core.feedback import (
                mostrar_feedback,
            )

            mostrar_feedback(
                page,
                "Não existem médias disponíveis para gerar o PDF.",
                sucesso=False,
            )

            return

        # --------------------------------------------------
        # SEMESTRE
        # --------------------------------------------------

        semestre_pdf = (
            semestre_atual
            if semestre_atual is not None
            else "Todos"
        )

        # --------------------------------------------------
        # QUANTIDADE DE AVALIAÇÕES
        # --------------------------------------------------

        quantidade_avaliacoes = len(
            resultados_filtrados
        )

        # --------------------------------------------------
        # CURSOS
        # --------------------------------------------------

        cursos = sorted(
            {
                normalizar_nome_curso(
                    resultado.get(
                        "curso_nome",
                        resultado.get("curso", "")
                    )
                )
                for resultado in resultados_filtrados
                if resultado.get("curso_nome")
                or resultado.get("curso")
            }
        )
        # --------------------------------------------------
        # GERAR PDF
        # --------------------------------------------------

        gerar_pdf_completo(
            page,
            medias=medias_validas,
            nomes_eixos=NOMES_EIXOS,
            semestre=semestre_pdf,
            quantidade_avaliacoes=quantidade_avaliacoes,
            cursos=cursos,
        )
        
    # ==================================================
    # TABELA
    # ==================================================
    
    tabela_resultados = criar_tabela_resultados(
        page,
        layout,
        borda_container,
        exportar_csv_atual,
        exportar_pdf_atual,
    )

    # ==================================================
    # APLICAR FILTROS
    # ==================================================

    def aplicar_filtros(
        semestre: str | None,
        eixo: int | None,
    ) -> None:

        nonlocal resultados_filtrados
        nonlocal semestre_atual
        nonlocal eixo_atual

        semestre_atual = semestre
        eixo_atual = eixo

        resultados_filtrados = filtrar_resultados(
            resultados_originais,
            semestre=semestre,
            eixo=eixo,
        )

        # --------------------------------------------------
        # ATUALIZAR DASHBOARD
        # --------------------------------------------------

        if hasattr(
            dashboard_visual,
            "atualizar",
        ):

            dashboard_visual.atualizar(
                semestre,
                eixo,
            )

        # --------------------------------------------------
        # ATUALIZAR TABELA
        # --------------------------------------------------

        if hasattr(
            tabela_resultados.content.controls[2],
            "atualizar",
        ):

            tabela_resultados.content.controls[2].atualizar(
                semestre,
                eixo,
            )

        page.update()

    # ==================================================
    # FILTROS
    # ==================================================

    secao_filtros = criar_secao_filtros(
        layout,
        borda_container,
        page,
        aplicar_filtros,
        exportar_csv_atual,
        exportar_pdf_atual,
    )

    # ==================================================
    # ABA DE DADOS
    # ==================================================

    conteudo_aba_dados = ft.Container(
        expand=True,
        padding=ft.Padding.only(
            top=20
        ),
        content=ft.Column(
            expand=True,
            controls=[
                tabela_resultados
            ],
        ),
    )

    # ==================================================
    # ABAS
    # ==================================================

    barra_abas = ft.TabBar(
        tabs=[
            ft.Tab(
                label="Dashboard Executivo",
                icon=ft.Icons.DASHBOARD,
            ),
            ft.Tab(
                label="Dados Brutos e Exportação",
                icon=ft.Icons.TABLE_CHART,
            ),
        ],
        label_color=COR_PRIMARIA,
        unselected_label_color=ft.Colors.GREY_600,
        indicator_color=COR_PRIMARIA,
        divider_color=layout.cores[BORDA],
    )

    conteudo_abas = ft.TabBarView(
        expand=True,
        controls=[
            dashboard_visual,
            conteudo_aba_dados,
        ],
    )
    
    indice_aba_relatorios = getattr(
        page,
        "indice_aba_relatorios",
        0,
    )
    
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
            controls=[
                barra_abas,
                conteudo_abas,
            ],
        ),
    )

    # ==================================================
    # CONTEÚDO PRINCIPAL
    # ==================================================

    conteudo = ft.Column(
        expand=True,
        controls=[
            secao_filtros,
            ft.Container(height=10),
            abas,
        ],
    )

    # ==================================================
    # FINALIZAÇÃO
    # ==================================================

    layout.add_content(
        conteudo
    )

    return layout.criar_view(
        "/relatorios"
    )