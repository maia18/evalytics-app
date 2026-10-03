import logging
import os
from datetime import datetime
from typing import Optional

import flet as ft

from models.avaliacoes.core.feedback import mostrar_feedback
from models.relatorios.core.pdf_template import RelatorioEvalytics
from models.relatorios.core.grafico_radar import salvar_grafico_radar


logger = logging.getLogger(__name__)

CAMINHO_IMAGEM_TEMP = "radar_temp.png"


def gerar_pdf_completo(
    page: ft.Page,
    medias: dict[int, float | None],
    nomes_eixos: dict[int, str],
    semestre: str = "Todos",
) -> Optional[str]:
    """
    Gera o relatório PDF utilizando as médias fornecidas.

    As médias devem vir da mesma camada de relatórios utilizada
    pelo Dashboard, respeitando os filtros selecionados.
    """

    try:
        # ==================================================
        # VALIDAÇÃO DAS MÉDIAS
        # ==================================================

        medias_validas = {}

        for eixo_id, nota in medias.items():
            if nota is None:
                continue

            try:
                medias_validas[eixo_id] = float(nota)
            except (TypeError, ValueError):
                continue

        if not medias_validas:
            mostrar_feedback(
                page,
                "Não existem dados para gerar o relatório PDF.",
                sucesso=False,
            )
            return None

        # ==================================================
        # GRÁFICO RADAR
        # ==================================================

        salvar_grafico_radar(
            medias_validas,
            nomes_eixos,
            CAMINHO_IMAGEM_TEMP,
        )

        # ==================================================
        # DOCUMENTO
        # ==================================================

        pdf = RelatorioEvalytics(
            orientation="P",
            unit="mm",
            format="A4",
        )

        pdf.set_left_margin(20)
        pdf.set_right_margin(20)

        pdf.add_page()

        # ==================================================
        # DATA DE GERAÇÃO
        # ==================================================

        pdf.set_font(
            "helvetica",
            "I",
            10,
        )

        pdf.set_text_color(
            100,
            100,
            100,
        )

        data_geracao = datetime.now().strftime(
            "%d/%m/%Y às %H:%M"
        )

        pdf.cell(
            0,
            5,
            f"Documento gerado em: {data_geracao}",
            ln=True,
            align="R",
        )

        pdf.ln(5)

        # ==================================================
        # INTRODUÇÃO
        # ==================================================

        pdf.set_font(
            "helvetica",
            "",
            12,
        )

        pdf.set_text_color(
            0,
            0,
            0,
        )

        texto_intro = (
            "Este relatório apresenta os resultados das "
            "avaliações institucionais coletadas através "
            "da plataforma Evalytics. Os dados apresentados "
            "correspondem aos filtros selecionados na tela "
            "de Relatórios."
        )

        pdf.multi_cell(
            0,
            7,
            txt=texto_intro,
            align="J",
        )

        pdf.ln(5)

        # ==================================================
        # FILTRO DE SEMESTRE
        # ==================================================

        pdf.set_font(
            "helvetica",
            "B",
            11,
        )

        pdf.cell(
            0,
            7,
            f"Semestre: {semestre}",
            ln=True,
        )

        pdf.ln(3)

        # ==================================================
        # GRÁFICO
        # ==================================================

        if os.path.exists(CAMINHO_IMAGEM_TEMP):
            pdf.image(
                CAMINHO_IMAGEM_TEMP,
                x=55,
                w=100,
            )

            pdf.ln(10)

        # ==================================================
        # TABELA
        # ==================================================

        pdf.set_font(
            "helvetica",
            "B",
            11,
        )

        pdf.set_fill_color(
            240,
            240,
            240,
        )

        largura_semestre = 30

        qtde_eixos = len(
            medias_validas
        )

        largura_coluna_eixo = (
            140 / qtde_eixos
        )

        # --------------------------------------------------
        # CABEÇALHO
        # --------------------------------------------------

        pdf.cell(
            largura_semestre,
            10,
            "Semestre",
            border=1,
            fill=True,
            align="C",
        )

        for eixo_id in sorted(
            medias_validas.keys()
        ):
            nome_eixo = nomes_eixos.get(
                eixo_id,
                f"Eixo {eixo_id}",
            )

            pdf.cell(
                largura_coluna_eixo,
                10,
                nome_eixo.upper(),
                border=1,
                fill=True,
                align="C",
            )

        pdf.ln()

        # --------------------------------------------------
        # VALORES
        # --------------------------------------------------

        pdf.set_font(
            "helvetica",
            "",
            11,
        )

        pdf.cell(
            largura_semestre,
            10,
            semestre,
            border=1,
            align="C",
        )

        for eixo_id in sorted(
            medias_validas.keys()
        ):
            pdf.cell(
                largura_coluna_eixo,
                10,
                f"{medias_validas[eixo_id]:.2f}",
                border=1,
                align="C",
            )

        pdf.ln()

        # ==================================================
        # RESUMO
        # ==================================================

        pdf.ln(8)

        media_geral = (
            sum(medias_validas.values())
            / len(medias_validas)
        )

        pdf.set_font(
            "helvetica",
            "B",
            12,
        )

        pdf.cell(
            0,
            8,
            f"Média geral dos eixos respondidos: "
            f"{media_geral:.2f}",
            ln=True,
        )

        pdf.cell(
            0,
            8,
            f"Eixos considerados: "
            f"{len(medias_validas)}",
            ln=True,
        )

        # ==================================================
        # ARQUIVO
        # ==================================================

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        nome_arquivo = (
            f"relatorio_evalytics_{timestamp}.pdf"
        )

        pdf.output(
            nome_arquivo
        )

        # ==================================================
        # LIMPEZA
        # ==================================================

        if os.path.exists(
            CAMINHO_IMAGEM_TEMP
        ):
            os.remove(
                CAMINHO_IMAGEM_TEMP
            )

        # ==================================================
        # FEEDBACK
        # ==================================================

        mostrar_feedback(
            page,
            f"PDF gerado com sucesso: {nome_arquivo}",
            sucesso=True,
        )

        return nome_arquivo

    except Exception:
        if os.path.exists(
            CAMINHO_IMAGEM_TEMP
        ):
            os.remove(
                CAMINHO_IMAGEM_TEMP
            )

        logger.exception(
            "Erro ao gerar o documento PDF."
        )

        mostrar_feedback(
            page,
            "Erro ao gerar o documento PDF.",
            sucesso=False,
        )

        return None