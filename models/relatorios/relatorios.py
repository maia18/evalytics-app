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
from models.relatorios.core.export_pdf import gerar_pdf_completo


NOMES_EIXOS = {
    1: "Organização Didático-Pedagógica",
    2: "Corpo Docente e Tutorial",
    3: "Infraestrutura",
}


def ViewRelatorios(
    page: ft.Page,
    mudar_tela: Callable[[str], None],
) -> ft.View:

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

    # ======================================================
    # RESULTADOS REAIS
    # ======================================================

    resultados_originais = listar_resultados_avaliacoes()

    # Mantém os resultados atualmente exibidos.
    resultados_filtrados = list(resultados_originais)

    # Guarda os filtros atualmente aplicados.
    semestre_atual = None
    eixo_atual = None

    # ======================================================
    # DASHBOARD
    # ======================================================

    dashboard_visual = TelaResultados(page)

    # ======================================================
    # TABELA
    # ======================================================

    tabela_resultados = criar_tabela_resultados(
        page,
        layout,
        borda_container,
    )

    # ======================================================
    # EXPORTAÇÃO CSV
    # ======================================================

    def exportar_csv_atual(e=None) -> None:
        """
        Exporta exatamente os resultados atualmente
        exibidos pelos filtros.
        """

        exportar_csv(
            page,
            resultados=list(resultados_filtrados),
        )

    # ======================================================
    # CÁLCULO DAS MÉDIAS PARA O PDF
    # ======================================================

    def calcular_medias_pdf() -> dict[int, float | None]:
        """
        Calcula as médias dos eixos utilizando somente
        os resultados atualmente filtrados.

        Eixos sem respostas não entram no cálculo.
        """

        acumuladores = {
            1: [],
            2: [],
            3: [],
        }

        for resultado in resultados_filtrados:

            eixos = resultado.get("eixos", {})

            if not isinstance(eixos, dict):
                continue

            for eixo_id in (1, 2, 3):

                valor = eixos.get(eixo_id)

                if valor is None:
                    continue

                try:
                    valor = float(valor)
                except (TypeError, ValueError):
                    continue

                # Ausência de resposta.
                # Não transforma ausência em nota.
                if valor <= 0:
                    continue

                acumuladores[eixo_id].append(valor)

        medias = {}

        for eixo_id, notas in acumuladores.items():

            if notas:
                medias[eixo_id] = sum(notas) / len(notas)
            else:
                medias[eixo_id] = None

        return medias

    # ======================================================
    # EXPORTAÇÃO PDF
    # ======================================================

    def exportar_pdf_atual(e=None) -> None:
        print("DEBUG: exportar_pdf_atual foi chamada.")

        if not resultados_filtrados:
            from models.avaliacoes.core.feedback import mostrar_feedback

            mostrar_feedback(
                page,
                "Não existem dados para gerar o PDF.",
                sucesso=False,
            )
            return

        medias = calcular_medias_pdf()

        print("DEBUG: médias calculadas:", medias)

        medias_validas = {
            eixo_id: media
            for eixo_id, media in medias.items()
            if media is not None
        }

        print("DEBUG: médias válidas:", medias_validas)

        if not medias_validas:
            from models.avaliacoes.core.feedback import mostrar_feedback

            mostrar_feedback(
                page,
                "Não existem médias disponíveis para gerar o PDF.",
                sucesso=False,
            )
            return

        semestre_pdf = (
            semestre_atual
            if semestre_atual is not None
            else "Todos"
        )

        print("DEBUG: chamando gerar_pdf_completo...")

        gerar_pdf_completo(
            page,
            medias=medias_validas,
            nomes_eixos=NOMES_EIXOS,
            semestre=semestre_pdf,
        )

        print("DEBUG: gerar_pdf_completo terminou.")

    # ======================================================
    # APLICA FILTROS
    # ======================================================

    def aplicar_filtros(
        semestre: str | None,
        eixo: int | None,
    ) -> None:

        nonlocal resultados_filtrados
        nonlocal semestre_atual
        nonlocal eixo_atual

        # --------------------------------------------------
        # Guarda filtros atuais
        # --------------------------------------------------

        semestre_atual = semestre
        eixo_atual = eixo

        # --------------------------------------------------
        # Filtra os dados reais
        # --------------------------------------------------

        resultados_filtrados = filtrar_resultados(
            resultados_originais,
            semestre=semestre,
            eixo=eixo,
        )

        # --------------------------------------------------
        # Dashboard
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
        # Tabela
        # --------------------------------------------------

        if hasattr(
            tabela_resultados.content.controls[2],
            "atualizar",
        ):
            tabela_resultados.content.controls[2].atualizar(
                semestre,
                eixo,
            )

        # --------------------------------------------------
        # Atualiza interface
        # --------------------------------------------------

        page.update()

    # ======================================================
    # FILTROS
    # ======================================================

    secao_filtros = criar_secao_filtros(
        layout,
        borda_container,
        page,
        aplicar_filtros,
        exportar_csv_atual,
        exportar_pdf_atual,
    )

    # ======================================================
    # ABA DE DADOS
    # ======================================================

    conteudo_aba_dados = ft.Container(
        expand=True,
        padding=ft.Padding.only(top=20),
        content=ft.Column(
            expand=True,
            controls=[
                tabela_resultados,
            ],
        ),
    )

    # ======================================================
    # BARRA DE ABAS
    # ======================================================

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

    # ======================================================
    # CONTEÚDO DAS ABAS
    # ======================================================

    conteudo_abas = ft.TabBarView(
        expand=True,
        controls=[
            dashboard_visual,
            conteudo_aba_dados,
        ],
    )

    abas = ft.Tabs(
        length=2,
        selected_index=0,
        animation_duration=300,
        expand=True,
        content=ft.Column(
            expand=True,
            controls=[
                barra_abas,
                conteudo_abas,
            ],
        ),
    )

    # ======================================================
    # CONTEÚDO FINAL
    # ======================================================

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