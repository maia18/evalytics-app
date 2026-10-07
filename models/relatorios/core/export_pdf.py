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


def normalizar_nome_curso(nome: str) -> str:
    if not nome:
        return "Curso não informado"

    nome_limpo = str(nome).strip().lower()

    mapeamento = {
        "eng telecom": "Engenharia de Telecomunicações",
        "engenharia de telecomunicações": "Engenharia de Telecomunicações",
    }

    return mapeamento.get(
        nome_limpo,
        str(nome).strip(),
    )


def gerar_pdf_completo(
    page: ft.Page,
    medias: dict[int, float | None],
    nomes_eixos: dict[int, str],
    semestre: str = "Todos",
    quantidade_avaliacoes: int = 0,
    cursos: list[str] | None = None,
) -> Optional[str]:

    try:
        # ==================================================
        # VALIDAÇÃO DAS MÉDIAS
        # ==================================================

        medias_validas: dict[int, float] = {}

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
        # NORMALIZAÇÃO DOS CURSOS
        # ==================================================

        cursos_normalizados = {
            normalizar_nome_curso(curso)
            for curso in (cursos or [])
            if curso and str(curso).strip()
        }

        cursos_validos = sorted(cursos_normalizados)

        if cursos_validos:
            texto_cursos = ", ".join(cursos_validos)
        else:
            texto_cursos = "Todos os cursos"

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
            8,
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
            4,
            f"Documento gerado em: {data_geracao}",
            ln=True,
            align="R",
        )

        pdf.ln(2)

        # ==================================================
        # TÍTULO
        # ==================================================

        pdf.set_font(
            "helvetica",
            "B",
            18,
        )

        pdf.set_text_color(
            17,
            24,
            39,
        )

        pdf.cell(
            0,
            8,
            "Relatório de Avaliação Institucional",
            ln=True,
            align="C",
        )

        pdf.set_font(
            "helvetica",
            "",
            10,
        )

        pdf.set_text_color(
            95,
            99,
            104,
        )

        pdf.cell(
            0,
            5,
            "Evalytics",
            ln=True,
            align="C",
        )

        pdf.ln(4)

        # ==================================================
        # INTRODUÇÃO
        # ==================================================

        pdf.set_font(
            "helvetica",
            "",
            9,
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
            4.5,
            txt=texto_intro,
            align="J",
        )

        pdf.ln(3)

        # ==================================================
        # INFORMAÇÕES DO RELATÓRIO
        # ==================================================

        pdf.set_font(
            "helvetica",
            "B",
            11,
        )

        pdf.set_text_color(
            17,
            24,
            39,
        )

        pdf.cell(
            0,
            6,
            "Informações do relatório",
            ln=True,
        )

        pdf.ln(1)

        largura_rotulo = 40
        largura_valor = 130
        altura_linha = 6

        pdf.set_fill_color(
            245,
            245,
            245,
        )

        # --------------------------------------------------
        # SEMESTRE
        # --------------------------------------------------

        pdf.set_font(
            "helvetica",
            "B",
            9,
        )

        pdf.cell(
            largura_rotulo,
            altura_linha,
            "Semestre",
            border=1,
            fill=True,
            align="L",
        )

        pdf.set_font(
            "helvetica",
            "",
            9,
        )

        pdf.cell(
            largura_valor,
            altura_linha,
            str(semestre),
            border=1,
            align="L",
        )

        pdf.ln()

        # --------------------------------------------------
        # CURSO
        # --------------------------------------------------

        pdf.set_font(
            "helvetica",
            "B",
            9,
        )

        pdf.cell(
            largura_rotulo,
            altura_linha,
            "Curso(s)",
            border=1,
            fill=True,
            align="L",
        )

        pdf.set_font(
            "helvetica",
            "",
            9,
        )

        pdf.cell(
            largura_valor,
            altura_linha,
            texto_cursos,
            border=1,
            align="L",
        )

        pdf.ln()

        # --------------------------------------------------
        # AVALIAÇÕES
        # --------------------------------------------------

        pdf.set_font(
            "helvetica",
            "B",
            9,
        )

        pdf.cell(
            largura_rotulo,
            altura_linha,
            "Avaliações",
            border=1,
            fill=True,
            align="L",
        )

        pdf.set_font(
            "helvetica",
            "",
            9,
        )

        pdf.cell(
            largura_valor,
            altura_linha,
            str(quantidade_avaliacoes),
            border=1,
            align="L",
        )

        pdf.ln(5)

        # ==================================================
        # GRÁFICO RADAR
        # ==================================================

        if os.path.exists(CAMINHO_IMAGEM_TEMP):

            pdf.set_font(
                "helvetica",
                "B",
                11,
            )

            pdf.set_text_color(
                17,
                24,
                39,
            )

            pdf.cell(
                0,
                6,
                "Desempenho por eixo avaliativo",
                ln=True,
                align="C",
            )

            pdf.ln(1)

            # Radar menor para preservar espaço vertical.
            pdf.image(
                CAMINHO_IMAGEM_TEMP,
                x=67,
                w=76,
            )

            pdf.ln(3)

        # ==================================================
        # TABELA DE MÉDIAS
        # ==================================================

        pdf.set_font(
            "helvetica",
            "B",
            11,
        )

        pdf.set_text_color(
            17,
            24,
            39,
        )

        pdf.cell(
            0,
            6,
            "Médias por eixo avaliativo",
            ln=True,
        )

        pdf.ln(1)

        largura_eixo = 140
        largura_nota = 30
        altura_tabela = 7

        pdf.set_font(
            "helvetica",
            "B",
            9,
        )

        pdf.set_fill_color(
            240,
            240,
            240,
        )

        # --------------------------------------------------
        # CABEÇALHO
        # --------------------------------------------------

        pdf.cell(
            largura_eixo,
            altura_tabela,
            "Eixo avaliativo",
            border=1,
            fill=True,
            align="C",
        )

        pdf.cell(
            largura_nota,
            altura_tabela,
            "Média",
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
            9,
        )

        for eixo_id in sorted(
            medias_validas.keys()
        ):

            nome_eixo = nomes_eixos.get(
                eixo_id,
                f"Eixo {eixo_id}",
            )

            nota = medias_validas[eixo_id]

            pdf.cell(
                largura_eixo,
                altura_tabela,
                nome_eixo,
                border=1,
                align="L",
            )

            pdf.cell(
                largura_nota,
                altura_tabela,
                f"{nota:.2f}",
                border=1,
                align="C",
            )

            pdf.ln()

        # ==================================================
        # RESUMO
        # ==================================================

        media_geral = (
            sum(medias_validas.values())
            / len(medias_validas)
        )

        pdf.ln(4)

        pdf.set_font(
            "helvetica",
            "B",
            11,
        )

        pdf.set_text_color(
            17,
            24,
            39,
        )

        pdf.cell(
            0,
            6,
            "Resumo dos resultados",
            ln=True,
        )

        pdf.set_font(
            "helvetica",
            "",
            9,
        )

        pdf.cell(
            0,
            5,
            f"Média geral dos eixos respondidos: {media_geral:.2f}",
            ln=True,
        )

        pdf.cell(
            0,
            5,
            f"Eixos considerados: {len(medias_validas)}",
            ln=True,
        )

        pdf.cell(
            0,
            5,
            f"Avaliações analisadas: {quantidade_avaliacoes}",
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